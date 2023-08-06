import importlib.util
import os


class BanquetHandler:
    def __init__(self, conf, path=None):
        self.handler = None
        self._base = path
        self.path = os.path.join(os.getcwd(), path)
        self.summary = conf.get("summary")
        self.gateway = conf.get("x-amazon-apigateway-integration")
        self.handler_path = conf.get("x-handler")

        self.load()

    def load(self):
        if self.handler_path is None:
            return

        fp = None

        try:
            spec = importlib.util.spec_from_file_location(
                self.handler_path,
                os.path.join(self.path, self.handler_path, "index.py"),
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        except ImportError:
            raise Exception(
                f"Unable to find handler {self.handler_path} in {self._base}"
            )
        finally:
            if fp:
                fp.close()

        self.handler = mod.handler

    def call(self, event, context):
        return self.handler(event, context)
