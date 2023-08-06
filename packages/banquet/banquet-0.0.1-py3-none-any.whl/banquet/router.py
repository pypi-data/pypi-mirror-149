import re

from .handler import BanquetHandler

URL_PATH_PARAM = re.compile(r"\{(.+?)\}")


class BanquetRouter:
    def __init__(self, openapi_spec, functions_path):
        self.openapi_spec = openapi_spec
        self.functions_path = functions_path
        self.routes = {
            "GET": {},
            "POST": {},
            "DELETE": {},
        }
        self.setup_from_openapi()

    def setup_from_openapi(self):
        for url, config in self.openapi_spec["paths"].items():
            if "{" in url:
                for part in URL_PATH_PARAM.findall(url):
                    url = url.replace("{" + part + "}", f"(?P<{part}>.+?)")

                url = re.compile(f"^{url}$")

            for method, conf in config.items():
                method = method.upper()

                if method not in ["GET", "POST", "DELETE"]:
                    continue

                self.routes[method][url] = BanquetHandler(
                    conf, path=self.functions_path
                )

    def resolver(self, routes, path):
        if path in routes:
            return routes[path], None

        for route, handler in routes.items():
            if isinstance(route, re.Pattern):
                if route.match(path):
                    params = [m.groupdict() for m in route.finditer(path)][0]
                    return handler, params

        return None, None

    def resolve(self, method, path):
        return self.resolver(self.routes[method], path)
