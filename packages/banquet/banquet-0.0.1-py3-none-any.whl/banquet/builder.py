from itertools import chain


def build_spec_for_routes(routes):
    spec = {"paths": {}}

    for route in chain(*routes):
        method, url, function = route.split(":")

        spec["paths"][url] = {method: {"x-handler": function}}

    return spec
