from __future__ import print_function

from vswmc.cli import utils


def stop(args):
    client = utils.create_client(args)
    for run in args.run:
        client.stop_run(run)
        print("Stopped", run)


def configure_parser(parser):
    parser.set_defaults(func=stop)
    parser.add_argument("run", metavar="RUN", nargs="+", help="Run to stop")
