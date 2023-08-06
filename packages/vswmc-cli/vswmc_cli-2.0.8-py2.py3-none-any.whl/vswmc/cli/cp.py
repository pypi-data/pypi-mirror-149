from __future__ import print_function

import os

from vswmc.cli import utils


def do_cp(args):
    client = utils.create_client(args)

    run, src_file = args.src.split(":")

    content = client.download_result(run, src_file)

    _, src_filename = os.path.split(src_file)

    if os.path.isdir(args.dst):
        target_file = os.path.join(args.dst, src_filename)
    else:
        target_file = args.dst

    with open(target_file, "wb") as f:
        f.write(content)


def configure_parser(parser):
    parser.set_defaults(func=do_cp)
    parser.add_argument(
        "src", metavar="SRC", type=str, help="file in the format RUN:FILE"
    )
    parser.add_argument("dst", metavar="DST", type=str, help="target file or directory")
