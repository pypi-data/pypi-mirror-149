from __future__ import print_function

from vswmc.cli import utils


def rm(args):
    client = utils.create_client(args)
    for run in args.run:
        client.delete_run(run)
        print("Deleted", run)


def configure_parser(parser):
    parser.set_defaults(func=rm)
    parser.add_argument("run", metavar="RUN", nargs="+", help="Run to delete")
