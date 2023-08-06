from jupyter_server.utils import url_path_join

from .transform_view import TransformJupyterRouteHandler
from .autocomplete_view import AutoCompleteRouteHandler

TRANSFORM_NB_ROUTE = "TRANSFORM_NB"
AUTOCOMPLETE_ROUTE = "AUTOCOMPLETE"


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    url_path = "jupyterlab-mutableai"

    autocomplete_route_pattern = url_path_join(base_url, url_path, AUTOCOMPLETE_ROUTE)
    transform_jupyter_route_pattern = url_path_join(
        base_url, url_path, TRANSFORM_NB_ROUTE
    )

    handlers = [
        (autocomplete_route_pattern, AutoCompleteRouteHandler),
        (transform_jupyter_route_pattern, TransformJupyterRouteHandler),
    ]

    web_app.add_handlers(host_pattern, handlers)
