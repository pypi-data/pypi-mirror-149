from __future__ import print_function

from vswmc.cli import utils


def do_ls(args):
    client = utils.create_client(args)
    run = client.get_run(args.run)
    rows = []
    for result in run["results"]:
        if args.l:
            rows.append(
                [
                    str(result["size"]),
                    result["updated"],
                    result["path"],
                ]
            )
        else:
            rows.append([result["path"]])
    utils.print_table(rows)


def configure_parser(parser):
    parser.set_defaults(func=do_ls)
    parser.add_argument("run", metavar="RUN", help="The run to query")
    parser.add_argument("-l", action="store_true", help="Print long listing")
