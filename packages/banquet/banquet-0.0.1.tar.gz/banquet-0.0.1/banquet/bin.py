import argparse
import logging

from .server import run_server


def cli():
    parser = argparse.ArgumentParser(
        prog="banquet", description="Banquet development server"
    )

    parser.add_argument(
        "-r",
        "--routes",
        type=str,
        nargs="+",
        action="append",
        default=None,
        help="Specify routes individually in format method:path:function",
    )

    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=2424,
        help="Specify the port on which the server listens",
    )

    parser.add_argument(
        "-s",
        "--spec",
        default=None,
        help="Location of the api spec",
    )

    parser.add_argument(
        "-f",
        "--functions",
        default="functions/",
        help="Location of the functions",
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    run_server(
        args.listen, args.port, args.routes, spec=args.spec, functions=args.functions
    )
