from __future__ import print_function

from vswmc.cli import utils


def list_(args):
    client = utils.create_client(args)

    rows = [["ID", "NAME"]]
    for model in client.list_models():
        rows.append(
            [
                model["id"],
                model["name"],
            ]
        )
    utils.print_table(rows)


def describe(args):
    client = utils.create_client(args)
    model = client.get_model(args.model)
    print("Id:", model["id"])
    print("Name:", model["name"])
    print("Description:", model["description"] or "")


def configure_parser(parser):
    subparsers = parser.add_subparsers(title="Commands", metavar="COMMAND")
    subparsers.required = True

    subparser = subparsers.add_parser("list", help="List models")
    subparser.set_defaults(func=list_)

    subparser = subparsers.add_parser("describe", help="Describe a model")
    subparser.add_argument("model", metavar="MODEL", help="ID of the model to describe")
    subparser.set_defaults(func=describe)
