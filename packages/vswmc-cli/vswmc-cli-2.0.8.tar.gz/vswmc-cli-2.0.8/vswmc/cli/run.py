from __future__ import print_function

import os

from vswmc.cli import utils


def add_parameter(run_parameters, param):
    if "=" not in param:
        raise Exception("Invalid parameter '{}'. Use format 'key=value'".format(param))

    key, value = param.split("=")
    run_parameters[key] = value


def do_run(args):
    parameters = {}

    if args.param_file:
        with open(args.param_file, "rb") as f:
            for param in f.readlines():
                param = param.strip()
                if param and not param.startswith("#"):
                    add_parameter(parameters, param)

    for param_arg in args.param or []:
        for param in param_arg:
            add_parameter(parameters, param)

    client = utils.create_client(args)

    if "magnetogram" in parameters:
        path = os.path.expanduser(parameters["magnetogram"])
        with open(path, "rb") as f:
            name = os.path.basename(path)
            upload_reference = client.upload_magnetogram(f, name)
            parameters["magnetogram"] = upload_reference
    if "cmes" in parameters:
        path = os.path.expanduser(parameters["cmes"])
        with open(path, "rb") as f:
            name = os.path.basename(path)
            upload_reference = client.upload_cme_file(f, name)
            parameters["cmes"] = upload_reference["cmes"]

    run = client.start_run(args.simulation, parameters=parameters)

    def on_data(msg, sess):  # source, generated, msg
        print("{} [{}] {}".format(msg["generated"], msg["source"], msg["msg"]))
        if "Stopping run" in msg["msg"]:
            sess.disconnect()

    if args.follow:
        content = client.download_logs(run["id"]).strip()
        if content:
            print(content)
        subscription = client.follow_logs(args.user, run["id"], on_data=on_data)
        subscription.result()
    else:
        print(run["id"])


def configure_parser(parser):
    parser.set_defaults(func=do_run)
    parser.add_argument("--param-file", help="Read parameters from a file")
    parser.add_argument(
        "--param",
        metavar="PARAM=VALUE",
        action="append",
        nargs="+",
        help="Set parameters",
    )
    parser.add_argument("-f", "--follow", action="store_true", help="Follow log output")
    parser.add_argument(
        "simulation", metavar="SIMULATION", help="The simulation to run"
    )
