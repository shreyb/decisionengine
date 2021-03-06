#!/usr/bin/env python3

import argparse
import xmlrpc.client

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "product",
        metavar='<product>',
        help="product to query")
    parser.add_argument(
        "--format",
        metavar='<format>',
        help="Possible formats are 'csv', 'json'.")
    parser.add_argument(
        "--since",
        metavar='<time>',
        help="Minimum start time for task managers. "
             "If omitted, searches only the current task manager.\n"
             "(e.g. 2021-03-21 11:00:00)")
    parser.add_argument(
        "--port",
        metavar='<port number>',
        default="8888",
        help="Default port is 8888")
    parser.add_argument(
        "--host",
        metavar='<hostname>',
        default="localhost",
        help="Default hostname is 'localhost'")
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Include exception message in printout if server is inaccessible")

    return parser

def execute_command_from_args(argsparsed, de_socket):
    """Calls the proper function for the arguments passed to de_query_tool.

    Args:
        argsparsed (Namespace): Should be from create_parser in this file.
        de_socket (ServerProxy): RPC Server Proxy.

    Returns:
        str: Output of the command.
    """

    return de_socket.query_tool(argsparsed.product, argsparsed.format, argsparsed.since)

def main(args_to_parse=None):
    """Main function for de_query_tool

    Args:
        args_to_parse (list, optional): If you pass a list of args, they will be used instead of sys.argv. Defaults to None.

    Returns:
        str: Query result
    """

    parser = create_parser()
    args = parser.parse_args(args_to_parse)
    url = f"http://{args.host}:{args.port}"
    de_socket = xmlrpc.client.ServerProxy(url, allow_none=True)
    try:
        return execute_command_from_args(args, de_socket)
    except OSError as e:
        msg = f"An error occurred while trying to access a DE server at '{url}'\n" + \
            "Please ensure that the host and port names correspond to a running DE instance."
        if args.verbose:
            msg += f'\n{e}'
        return msg
    except Exception as e:  # pragma: no cover
        msg = f"An error occurred while trying to access a DE server at '{url}'."
        if args.verbose:
            msg += f'\n{e}'
        return msg


if __name__ == "__main__":
    print(main())
