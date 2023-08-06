import json

import requests

from vswmc.core.exceptions import NotFound, Unauthorized, VswmcError
from vswmc.sockjs import SockJSSession

SSO_URL = "https://sso.ssa.esa.int/am/json/authenticate"


class VswmcClient(object):
    def __init__(self, address, credentials=None):
        self.address = address
        self.auth_root = address + "/auth"
        self.api_root = address + "/api"
        self.eb_root = address + "/eventbus"

        self.session = requests.Session()
        if credentials:
            self.login(credentials)

    def login(self, credentials):
        self.session.cookies.clear()

        res = self.session.post(
            SSO_URL,
            headers={
                "X-OpenAM-Username": credentials.username,
                "X-OpenAM-Password": credentials.password,
            },
        )

        msg = res.json()
        if "tokenId" not in msg:
            code = msg["code"]
            reason = msg["reason"]
            message = msg["message"]
            if code == 401:
                raise Unauthorized("Authentication Failed")
            else:
                raise VswmcError(reason + ": " + message)

        token = msg["tokenId"]
        self.session.cookies.set("iPlanetDirectoryPro", token)
        self.session.cookies.set("esa-ssa-sso-cookie", token)

    def list_models(self):
        path = "{}/models".format(self.api_root)
        return self._request("get", path=path).json()["models"]

    def get_model(self, name):
        path = "{}/models/{}".format(self.api_root, name)
        return self._request("get", path=path).json()

    def list_simulations(self):
        path = "{}/simulations".format(self.api_root)
        return self._request("get", path=path).json()["simulations"]

    def get_simulation(self, id_):
        path = "{}/simulations/{}".format(self.api_root, id_)
        return self._request("get", path=path).json()

    def list_products(self, type=None, run=None):
        path = "{}/products".format(self.api_root)
        params = {}
        if type:
            params["productType"] = type
        if run:
            params["run"] = run
        return self._request("get", path=path, params=params).json()

    def get_product(self, id_):
        path = "{}/products/{}".format(self.api_root, id_)
        return self._request("get", path=path).json()

    def create_product(self, type, attachments, dry_run=False):
        path = "{}/products".format(self.api_root)
        data = {
            "productType": type,
            "attachments": attachments,
            "dryRun": dry_run,
        }
        return self._request("post", path=path, json=data).json()

    def list_runs(self, simulation=None, status=None):
        path = "{}/runs".format(self.api_root)
        params = {}
        if simulation:
            params["simulation"] = simulation
        if status:
            params["status"] = status
        response = self._request("get", path=path, params=params).json()
        return response["runs"] if "runs" in response else []

    def start_run(self, simulation, parameters=None):
        path = "{}/runs".format(self.api_root)
        converted_parameters = {k: json.dumps(parameters[k]) for k in parameters or {}}
        data = {
            "simulation": simulation,
            "variables": converted_parameters,
        }
        return self._request("post", path=path, json=data).json()

    def get_run(self, run):
        path = "{}/runs/{}".format(self.api_root, run)
        return self._request("get", path=path).json()

    def download_logs(self, run):
        path = "{}/runs/{}/log".format(self.api_root, run)
        return self._request("get", path=path, params={"raw": "yes"}).content

    def download_result(self, run, path):
        path = "{}/runs/{}/results/{}".format(self.api_root, run, path)
        return self._request("get", path=path).content

    def download_results(self, run):
        path = "{}/runs/{}/results".format(self.api_root, run)
        return self._request("get", path=path).content

    def follow_logs(self, user, run, on_data):
        def filter_(msg, sess):
            if run == msg["headers"]["runId"]:
                on_data(msg["body"], sess)

        session = SockJSSession(self.address, on_data=filter_, session=self.session)
        session.send(
            json.dumps(
                {
                    "type": "register",
                    "address": "http.user.{}.runlog".format(user),
                    "headers": {},
                }
            )
        )
        return session

    def stop_run(self, run):
        path = "{}/runs/{}/terminate".format(self.api_root, run)
        self._request("post", path=path)

    def delete_run(self, run):
        path = "{}/runs/{}/delete".format(self.api_root, run)
        self._request("post", path=path)

    def is_test(self):
        return "localhost" in self.address or "spaceweather2" in self.address

    def upload_magnetogram(self, f, name):
        if self.is_test():
            upload = self.upload_file(f, name)
            path = "{}/products/magnetograms/USER/{}".format(self.api_root, upload)
            return self._request("get", path=path).json()
        else:
            path = "{}/products/magnetograms".format(self.api_root)
            files = {"file": (name, f, "application/octet-stream")}
            return self._request("post", path=path, files=files).json()

    def upload_cme_file(self, f, name):
        if self.is_test():
            upload = self.upload_file(f, name)
            path = "{}/products/cme/{}".format(self.api_root, upload)
            return self._request("get", path=path).json()
        else:
            path = "{}/products/cme".format(self.api_root)
            files = {"file": (name, f, "application/octet-stream")}
            return self._request("post", path=path, files=files).json()

    def upload_file(self, f, name):
        path = "{}/uploads".format(self.api_root)
        files = {"file": (name, f, "application/octet-stream")}
        return self._request("post", path=path, files=files).json()["_id"]

    def _request(self, method, path, **kwargs):
        response = self.session.request(method, path, **kwargs)

        if response.headers.get("content-type", "").startswith("text/html"):
            if "OpenAM" in response.text:
                raise Unauthorized("Invalid session")

        if 200 <= response.status_code < 300:
            return response

        if response.status_code == 401:
            raise Unauthorized("401 Client Error: Unauthorized")
        elif response.status_code == 404:
            raise NotFound("404 Client Error: {}".format(response.content))
        elif 400 <= response.status_code < 500:
            raise VswmcError(
                "{} Client Error: {}".format(response.status_code, response.content)
            )
        raise VswmcError(
            "{} Server Error: {}".format(response.status_code, response.content)
        )
