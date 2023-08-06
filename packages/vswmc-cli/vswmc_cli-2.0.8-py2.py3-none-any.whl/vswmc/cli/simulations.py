from __future__ import print_function

from vswmc.cli import utils


def list_(args):
    client = utils.create_client(args)

    rows = [["ID", "NAME", "MODELS"]]
    for simulation in client.list_simulations():
        model_ids = [m["id"] for m in simulation["models"]]
        rows.append(
            [
                simulation["id"],
                simulation["name"],
                ", ".join(model_ids),
            ]
        )
    utils.print_table(rows)


def describe(args):
    client = utils.create_client(args)
    simulation = client.get_simulation(args.simulation)

    if simulation["inputs"]:
        for parameter in simulation["inputs"]:
            print(" - key: " + parameter["key"])
            print("   required: {}".format("yes" if parameter["required"] else "no"))
            if "choices" in parameter:
                keys = [choice["key"] for choice in parameter["choices"]]
                print("   choices: {}".format(", ".join(keys)))
    else:
        print("Parameters: None")


def configure_parser(parser):
    subparsers = parser.add_subparsers(title="Commands", metavar="COMMAND")
    subparsers.required = True

    subparser = subparsers.add_parser("list", help="List simulations")
    subparser.set_defaults(func=list_)

    subparser = subparsers.add_parser("describe", help="Describe a simulation")
    subparser.add_argument(
        "simulation", metavar="SIMULATION", help="ID of the simulation to describe"
    )
    subparser.set_defaults(func=describe)
