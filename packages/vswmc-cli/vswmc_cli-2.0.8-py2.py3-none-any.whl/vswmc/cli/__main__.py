from __future__ import print_function

import argparse
import logging

import pkg_resources
from vswmc.cli import (
    cp,
    logs,
    ls,
    models,
    products,
    ps,
    rm,
    run,
    save,
    simulations,
    stop,
)


class SubCommandHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _format_action(self, action):
        # Removes the subparsers metavar from the help output
        parts = super(SubCommandHelpFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts


def main():
    dist = pkg_resources.get_distribution("vswmc-cli")
    parser = argparse.ArgumentParser(
        description=None, formatter_class=SubCommandHelpFormatter
    )
    parser.add_argument(
        "--version",
        action="version",
        version=dist.version,
        help="Print version information and quit",
    )
    parser.add_argument(
        "-u", metavar="USER", dest="user", required=True, help="SSA Username"
    )
    parser.add_argument("-p", metavar="PASSWORD", dest="password", help="SSA Password")
    parser.add_argument("--dev", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--debug", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument(
        "--url", default="https://spaceweather.hpc.kuleuven.be", help=argparse.SUPPRESS
    )

    # The width of this impacts the command width of the command column :-/
    metavar = "COMMAND"

    subparsers = parser.add_subparsers(title="Commands", metavar=metavar)
    subparsers.required = True

    cp_parser = subparsers.add_parser("cp", help="Copy a result file to disk")
    cp.configure_parser(cp_parser)

    logs_parser = subparsers.add_parser("logs", help="Fetch the logs of a run")
    logs.configure_parser(logs_parser)

    ls_parser = subparsers.add_parser("ls", help="List the results of a run")
    ls.configure_parser(ls_parser)

    models_parser = subparsers.add_parser("models", help="Read models")
    models.configure_parser(models_parser)

    products_parser = subparsers.add_parser("products", help="List products")
    products.configure_parser(products_parser)

    ps_parser = subparsers.add_parser("ps", help="List runs")
    ps.configure_parser(ps_parser)

    rm_parser = subparsers.add_parser("rm", help="Remove one or more runs")
    rm.configure_parser(rm_parser)

    run_parser = subparsers.add_parser("run", help="Start a run")
    run.configure_parser(run_parser)

    save_parser = subparsers.add_parser("save", help="Save all results of a run")
    save.configure_parser(save_parser)

    simulations_parser = subparsers.add_parser("simulations", help="List simulations")
    simulations.configure_parser(simulations_parser)

    stop_parser = subparsers.add_parser("stop", help="Stop one or more runs")
    stop.configure_parser(stop_parser)

    args = parser.parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        print()
    except Exception as e:
        if args.debug:
            print(logging.traceback.format_exc())
        else:
            print(e)


if __name__ == "__main__":
    main()
