import json
import requests
import tornado
import os
import tarfile
import threading

from io import BytesIO
from jupyter_server.base.handlers import APIHandler
import base64


TRANSFORM_NB_ROUTE = "TRANSFORM_NB"


def create_file_packet(nb_filename: str) -> dict:
    """Create a file packet for the transform docker container
    Args:
      filename: the name of the file to be sent to the transform docker container
    Returns:
      A dict that is the file packet for the transform docker container
    """
    f = open(nb_filename, "rb").read()
    data = {
        "file_name": nb_filename,
        "file_data": base64.b64encode(f).decode("utf-8"),
    }
    return data


def call_transform_nb(
    filename: str, api_key: str, domain: str, mode: str, instruction: str = ""
) -> dict:
    """Call the transform docker container
    Args:
      filename: the name of the file to be sent to the transform docker container
    Returns:
      A dict that is the response from the transform docker container
    """
    data = create_file_packet(filename)
    data["mode"] = mode

    if instruction:
        data["instruction"] = instruction

    response = requests.post(
        url=os.path.join("https://", domain, TRANSFORM_NB_ROUTE),
        json=data,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
        },
    )
    return response


def threaded_transform(input_data):
    nb_filename = input_data["name"]
    instruction = input_data.get("instruction", "")

    api_key, domain, mode = (
        input_data["apiKey"],
        input_data["transformDomain"],
        input_data["mode"],
    )

    response = call_transform_nb(nb_filename, api_key, domain, mode, instruction)
    json_response = response.json()

    # get dirname of nb_filename
    dirname = os.path.dirname(nb_filename)

    # untar the tar file
    tar_file_content = base64.b64decode(json_response["tar_file_data"])

    # extract tar without writing to disk
    tar_file = tarfile.open(fileobj=BytesIO(tar_file_content), mode="r:gz")

    # save and extract to disk
    tar_file.extractall(path=dirname)


class TransformJupyterRouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(
            json.dumps({"data": "This is /jlab-ext-example/TRANSFORM_NB endpoint!"})
        )

    @tornado.web.authenticated
    def post(self):

        # input_data is a dictionary with a key "name"
        input_data = self.get_json_body()
        x = threading.Thread(target=threaded_transform, args=(input_data,))
        x.start()

        self.finish(json.dumps("processing transformation"))
