from __future__ import print_function

from vswmc.cli import utils


def on_data(msg, sess):
    print("{} [{}] {}".format(msg["generated"], msg["source"], msg["msg"]))
    if "Stopping run" in msg["msg"]:
        sess.disconnect()


def do_logs(args):
    client = utils.create_client(args)

    content = client.download_logs(args.run).strip()
    if content:
        print(content.strip())

    if args.follow:
        subscription = client.follow_logs(args.user, args.run, on_data=on_data)
        subscription.result()


def configure_parser(parser):
    parser.set_defaults(func=do_logs)
    parser.add_argument("run", metavar="RUN", help="The target run")
    parser.add_argument("-f", "--follow", action="store_true", help="Follow log output")
