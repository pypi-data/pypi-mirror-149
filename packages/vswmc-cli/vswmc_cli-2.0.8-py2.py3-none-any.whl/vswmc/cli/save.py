from __future__ import print_function

from vswmc.cli import utils


def do_save(args):
    client = utils.create_client(args)
    content = client.download_results(args.run)

    target_file = args.run + ".zip"
    print("Saving {}".format(target_file))
    with open(target_file, "wb") as f:
        f.write(content)


def configure_parser(parser):
    parser.set_defaults(func=do_save)
    parser.add_argument("run", metavar="RUN", help="The run to save")
