from __future__ import print_function

from vswmc.cli import utils


def ps(args):
    client = utils.create_client(args)
    kwargs = {
        "simulation": args.simulation,
    }

    if not args.all:
        kwargs["status"] = "ongoing"

    rows = [["ID", "NAME", "STATUS", "SUBMITTED", "STARTED", "FINISHED"]]
    for run in client.list_runs(**kwargs):
        name = "{} #{}".format(run["simulation"]["name"], int(run["counter"]))
        submitted = run["submitted"] if "submitted" in run else ""
        started = run["started"] if "started" in run else ""
        finished = run["finished"] if "finished" in run else ""
        rows.append([run["id"], name, run["state"], submitted, started, finished])
    utils.print_table(rows)


def configure_parser(parser):
    parser.set_defaults(func=ps)
    parser.add_argument("--simulation", type=str, help="Filter on simulation")
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="List all runs (default shows only ongoing)",
    )
