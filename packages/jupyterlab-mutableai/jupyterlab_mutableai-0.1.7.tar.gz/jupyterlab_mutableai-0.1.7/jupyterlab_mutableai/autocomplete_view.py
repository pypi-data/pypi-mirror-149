import json
import requests
import tornado
import os

from jupyter_server.base.handlers import APIHandler

AUTOCOMPLETE_ROUTE = "AUTOCOMPLETE"


def call_autocomplete(input_txt: str, api_key: str, domain: str) -> str:
    prompt = {"prompt": input_txt, "max_length": 150}
    rt_json = requests.post(
        url=os.path.join("https://", domain, AUTOCOMPLETE_ROUTE),
        json=prompt,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
        },
    ).json()

    if rt_json.get("message") == "Limit Exceeded":
        return "# Limit Exceeded"

    return rt_json["completion"]


class AutoCompleteRouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(
            json.dumps({"data": "This is /jlab-ext-example/AUTOCOMPLETE endpoint!"})
        )

    @tornado.web.authenticated
    def post(self):
        # input_data is a dictionary with a key "name"
        input_data = self.get_json_body()
        data_packet = str(input_data["line"])
        autocomplete_data = ""

        api_key, domain, flag = (
            input_data["apiKey"],
            input_data["domain"],
            input_data["flag"],
        )
        # If flag is set to false then we response with empty array.

        if flag:
            autocomplete_data = call_autocomplete(data_packet, api_key, domain)
        else:
            autocomplete_data = []

        self.finish(json.dumps(autocomplete_data))
