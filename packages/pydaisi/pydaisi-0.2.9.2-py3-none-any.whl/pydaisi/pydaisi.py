# Copyright 2022 Belmont Technology
from unittest import result
import os
import uuid
import codecs
import dill
import json
import logging
import trio
import httpx

from dotenv import dotenv_values
from rich import pretty
from rich.logging import RichHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
_loghandler = RichHandler(markup=True)
_loghandler.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="[%X]"))
logger.addHandler(_loghandler)

pretty.install()

daisi_base_url = "https://app.daisi.io"
daisi_base_route = "/pebble-api/pebbles"
daisi_new_route = "/pebble-api/daisies"


def _load_dill_string(s):  # pragma: no cover
    return dill.loads(codecs.decode(s.encode(), "base64"))


def _get_dill_string(obj):  # pragma: no cover
    return codecs.encode(dill.dumps(obj, protocol=5), "base64").decode()


def _is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


class DaisiResponseNotReady(Exception):
    def __init__(self, status):
        self.status = status


class DaisiExecutionError(RuntimeError):
    def __init__(self, status):
        self.status = status


class DaisiBulkExecution:
    def __init__(self, daisi, endpoint: str, arguments: list):
        self.daisi = daisi

        self.executions = []
        for args in arguments:
            de = DaisiExecution(
                id = str(uuid.uuid4()),
                daisi = daisi,
                endpoint = endpoint,
                arguments = args
            )

            self.executions.append(de)

        self._result = None

    def _bulk_fetch_result(self):
        if self._result:
            return self._result

        my_exec = []
        for execution in self.executions:
            my_exec.append({"id": str(execution.id), "arguments": execution.arguments})

        # Call the specified Daisi compute
        r = self.daisi.session.post(
            f"{self.daisi.base_url}/{self.daisi.id}/results_bulk",
            headers=self.daisi.headers,
            json={"executions": my_exec}
        )

        self._result = r.json()

        return self._result


class DaisiExecution:
    def __init__(self, daisi, endpoint: str, arguments: dict, id=None):
        self.id = id
        self.daisi = daisi
        self.endpoint = endpoint
        self.arguments = arguments
        self.last_status = "NOT_STARTED"
        self._result = None
        self.value_fetched = False

        # Prepare the arguments
        parsed_args = self._pickle_hidden(self.arguments)
        parsed_args["_endpoint"] = self.endpoint

        self.parsed_args = parsed_args

    def _store_pickle(self, data):
        my_args = {"data": data}

        # Call the specified Daisi compute
        r = self.daisi.session.post(
            f"{self.daisi.base_url}/pickle", headers=self.daisi.headers, json=my_args
        )

        # Return the result
        return r.content.decode()

    def _pickle_hidden(self, args):
        final_args = {}
        for k, v in args.items():
            # First check if it's a DaisiExecution object
            if type(v) == DaisiExecution:
                # Grab the last result
                v = v._result["outputs"][-1]["data"]

            if not _is_jsonable(v):
                x = self._store_pickle(_get_dill_string(v))
                final_args[k] = "lookup:" + x
            else:
                final_args[k] = v
        return final_args

    async def _start_execution(self):
        if self.id is None:
            r = await self.daisi.asession.post(
                f"{self.daisi.base_url}/{self.daisi.id}/executions",
                headers=self.daisi.headers,
                json=self.parsed_args,
            )
            if not (r.status_code < 400):
                self.last_status = "FAILED"
                logger.error(f"Failed to create execution: {r.status_code}")
                raise DaisiExecutionError("Failed to create execution")
            self.id = r.json()["id"]

    async def get_status(self):
        if self.id is None:
            await self._start_execution()
        if self.last_status not in ["FINISHED", "FAILED"]:
            r = await self.daisi.asession.get(
                f"{self.daisi.base_url}/{self.daisi.id}/executions/{self.id}/status",
                headers=self.daisi.headers,
            )
            self.last_status = r.json()
        return self.last_status

    async def get_logs(self, limit: int = None):
        if self.id is None:
            await self._start_execution()
        limit_param = {"limit": limit} if limit is not None else None

        r = await self.daisi.asession.get(
            f"{self.daisi.base_url}/{self.daisi.id}/executions/{self.id}/logs",
            headers=self.daisi.headers,
            params=limit_param,
        )
        res = r.json()
        return res

    def _unpickle_hidden(self):
        final_outputs = []
        for item in self._result["outputs"]:
            if item["type"] in ["console-log", "data-grid"]:
                continue

            if type(item["data"]) == str and item["data"].startswith("lookup:"):
                # Get the binary data
                l_split = item["data"].split("lookup:")

                r = self.daisi.session.get(
                    f"{self.daisi.base_url}/pickle",
                    params={"lookup": l_split[1]},
                    headers=self.daisi.headers,
                )
                item["data"] = _load_dill_string(r.content.decode())

            final_outputs.append(item)
        self._result["outputs"] = final_outputs

    @property
    def value(self):
        return trio.run(self.fetch_result)

    async def fetch_result(
        self, timeout: int = 180
    ):  # Set to 180 by default for testing, otherwise logs timeout
        timer = 0
        if self.id is None:
            await self._start_execution()
        if not self.value_fetched:
            while not (await self.get_status() in ["FINISHED", "FAILED"]):
                await trio.sleep(1)
                timer += 1
                if timer >= timeout:
                    logger.info(
                        f"Daisi {self.daisi.name} has timed out after {timer} seconds"
                    )
                    raise DaisiResponseNotReady(self.last_status)

            r = await self.daisi.asession.get(
                f"{self.daisi.base_url}/{self.daisi.id}/executions/{self.id}/results",
                headers=self.daisi.headers,
            )
            self._result = r.json()
            self._unpickle_hidden()

            if self._result["outputs"][0].get("label") == "ERROR":
                self.last_status = "FAILED"

                error_id = self._result["outputs"][0]["data"]["id"]

                r = self.daisi.session.get(
                    f"{self.daisi.base_url}/outputs/html/{error_id}",
                    headers=self.daisi.headers,
                )
                self._result["outputs"][0]["data"] = r.content.decode()

            self.value_fetched = True

        if len(self._result["outputs"]) > 1:
            return [x["data"] for x in self._result["outputs"]]
        else:
            return self._result["outputs"][0]["data"]


class Daisi:
    """
    A utility to assist in developing Daisis for the Daisi platform.

    A tool for creating, validating, publishing, and updating daisis.

    :param daisi_id: A daisi name or UUID
    :param base_url: The default URL to use for connecting to the daisi
    :param access_token: access token for authorizing to the platform
    """

    session = httpx.Client()
    asession = httpx.AsyncClient()

    def __init__(
        self, daisi_id: str, *, base_url: str = daisi_base_url, access_token: str = ""
    ):
        """
        Daisi constructor method.


        :raises ValueError: DaisiID Not Found (Non-200 response)
        """
        self.id = None
        self.name = None
        self.description = None
        self.endpoints = None
        self.base_url = base_url + daisi_base_route
        access_token = (
            access_token
            or os.getenv("DAISI_ACCESS_TOKEN", "")
            or dotenv_values().get("DAISI_ACCESS_TOKEN", "")  # type: ignore
        )
        self.new_url = base_url + daisi_new_route
        self.headers = {}
        if access_token:
            self.headers.update({"Authorization": f"token {access_token}"})

        # Check if it's a valid uuid:
        try:
            check_uuid = uuid.UUID(daisi_id) is not None
        except Exception as e:
            check_uuid = False

        _endpoints = None
        if check_uuid:
            r = self.session.get(f"{self.base_url}/{daisi_id}", headers=self.headers)
            if not r.is_success:
                raise ValueError("The specified Daisi ID could not be found.")
            else:
                logger.info(f"Found existing Daisi: {r.json()['name']}")

                self.name = r.json()["name"]
                self.id = daisi_id
        else:
            logger.info(f"Calling {self.new_url}/connect?name={daisi_id}")
            r = self.session.get(
                f"{self.new_url}/connect",
                headers=self.headers,
                params={"name": daisi_id},
            )
            result = r.json()

            if r.is_success:
                result = r.json()

                self.name = daisi_id
                daisi_id = result["id"]

                logger.info(f"Found existing Daisi: {daisi_id}")

                self.id = daisi_id
                _endpoints = result["endpoints"]
            else:
                # TODO: Handle git repo connection here
                raise ValueError("That daisi could not be found.")

        # Call the specified Daisi endpoints
        if not _endpoints:
            r = self.session.get(
                f"{self.base_url}/{self.id}/endpoints", headers=self.headers
            )

            _endpoints = r.json() if r.is_success else {}

        self.endpoints = {x["name"]: x["schema"] for x in _endpoints}
        functionlist = list(self.endpoints.keys())
        for f in functionlist:
            # Sync / blocking version
            self.__setattr__(
                f,
                (
                    lambda f: (lambda _, *a, **kwa: _._run(f, True, a, kwa)).__get__(
                        self
                    )
                )(f),
            )

            # Async / non-blocking version
            self.__setattr__(
                f + "_",
                (
                    lambda f: (lambda _, *a, **kwa: _._run(f, False, a, kwa)).__get__(
                        self
                    )
                )(f),
            )

    def dispatch(self, _func="compute", *args, **kwargs):
        # call as daisi.dispatch("functionname", arg1, arg2, p3=arg3)
        # Possible conflict if the function takes a keyword argument also named "_func".
        # Could rename the param to "__", or just call using "_run()"

        kwargs = kwargs if kwargs is not None else {}
        param_names = [p["id"] for p in self.endpoints[_func]]
        kwargs.update(zip(param_names, args))

        # Grab a new DaisiExecution
        daisi_execution = DaisiExecution(daisi=self, endpoint=_func, arguments=kwargs)
        return self._run(_func, False, args, kwargs)

    def _run(
        self, _func="compute", wait_for_completion=True, args: tuple = (), kwargs=None
    ):
        kwargs = kwargs if kwargs is not None else {}
        param_names = [p["id"] for p in self.endpoints[_func]]
        kwargs.update(zip(param_names, args))

        # Grab a new DaisiExecution
        daisi_execution = DaisiExecution(daisi=self, endpoint=_func, arguments=kwargs)

        if wait_for_completion:
            trio.run(daisi_execution.fetch_result)

        return daisi_execution

    def _bulk_run(
        self, _func="compute", arguments=[]
    ):
        # Grab a new DaisiExecution
        daisi_bulk_execution = DaisiBulkExecution(daisi=self, endpoint=_func, arguments=arguments)

        my_exec = []
        for execution in daisi_bulk_execution.executions:
            my_exec.append({"id": str(execution.id), "arguments": execution.arguments})

        # Call the specified Daisi compute
        r = self.session.post(
            f"{self.base_url}/{self.id}/executions_bulk",
            headers=self.headers,
            json={"executions": my_exec}
        )

        return daisi_bulk_execution

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def get_daisies(base_url: str = daisi_base_url, access_token: str = ""):
        """
        Queries Daisi platform for a list of all current daisis.

        :return: List of daisis available on the Daisi platform.
        :rtype list
        """

        access_token = access_token or os.getenv("DAISI_ACCESS_TOKEN") or ""
        headers = {"Authorization": f"token {access_token}"} if access_token else {}

        r = httpx.get(
            f"{base_url}{daisi_new_route}",
            params={"pageSize": 10000, "page": 1},
            headers=headers,
        )
        result = r.json()

        daisi_list = []
        for section_data in result["data"]:
            if section_data["name"] != "Topics":
                section_request = httpx.get(
                    f'{base_url}{daisi_new_route}/section/{section_data["id"]}',
                    params={"pageSize": 10000, "page": 1},
                    headers=headers,
                )
                section_daisies = section_request.json()
                daisi_list.extend(
                    [
                        {
                            "id": daisi["id"],
                            "name": daisi["name"],
                            "description": daisi["description"],
                        }
                        for daisi in section_daisies["data"]["data"]
                    ]
                )

        daisi_list = sorted(daisi_list, key=lambda x: x["name"])

        return daisi_list

    @staticmethod
    def run_parallel(*executions: DaisiExecution):
        return trio.run(Daisi._parallel_run, *executions)

    @staticmethod
    async def _parallel_run(*executions: DaisiExecution):
        async with trio.open_nursery() as nursery:
            for execution in executions:
                nursery.start_soon(execution.fetch_result)
        return [await execution.fetch_result() for execution in executions]
