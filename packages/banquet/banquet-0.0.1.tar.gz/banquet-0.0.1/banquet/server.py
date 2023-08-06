import logging
import os.path
import sys
from http.server import HTTPServer

import yaml

from .builder import build_spec_for_routes
from .gateway import BanquetGateway
from .router import BanquetRouter

logger = logging.getLogger("banquet")


class BanquetServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, router):
        self.router = router
        super().__init__(server_address, RequestHandlerClass)

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self, router=self.router)


def run_server(addr, port, routes, spec, functions):
    if routes is not None:
        # If we have routes, build a spec and ignore the spec argument
        openapi_spec = build_spec_for_routes(routes)

    else:
        if spec is None or not os.path.exists(spec):
            logger.error(f"Unable to find OpenAPI Spec on path '{spec}'")
            sys.exit(1)

        with open(spec) as f:
            openapi_spec = yaml.safe_load(f)

    try:
        router = BanquetRouter(openapi_spec, functions)
        server = BanquetServer((addr, port), BanquetGateway, router)
    except Exception as e:
        logger.error(e)
        sys.exit(1)
    else:
        logger.info(f"Starting banquet server on {addr}:{port}...")
        server.serve_forever()
