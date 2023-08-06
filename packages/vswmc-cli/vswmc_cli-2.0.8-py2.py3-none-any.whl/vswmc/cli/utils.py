from __future__ import print_function

import os
import pickle
from getpass import getpass

from vswmc.client import VswmcClient
from vswmc.core import auth

HOME = os.path.expanduser("~")
CONFIG_DIR = os.path.join(os.path.join(HOME, ".config"), "vswmc-cli")
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, "credentials")


def create_client(args):
    # Bypass auth for local development
    if args.dev:
        return VswmcClient("http://localhost:3000")

    client = VswmcClient(args.url)

    logged_in = False
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "rb") as f:
            creds = pickle.load(f)
            if creds["username"] == args.user:
                client.session.cookies.update(creds["cookies"])
                # Quick check to test if this session is still functional
                try:
                    client.list_models()
                    logged_in = True
                except:
                    pass
    if not logged_in:
        password = args.password or getpass("Password: ")
        if not password:
            print("*** Password may not be null")
            return False

        credentials = auth.Credentials(username=args.user, password=password)
        client.login(credentials)
        save_session(args.user, client.session.cookies)

    return client


def save_session(username, cookies):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    with open(CREDENTIALS_FILE, "wb") as f:
        pickle.dump(
            {
                "username": username,
                "cookies": cookies,
            },
            f,
        )


def print_table(rows, header=False):
    widths = list(map(len, rows[0]))
    for row in rows:
        for idx, col in enumerate(row):
            widths[idx] = max(len(str(col)), widths[idx])

    separator = "  "

    total_width = 0
    for width in widths:
        total_width += width
    total_width += len(separator) * (len(widths) - 1)

    data = rows[1:] if header else rows
    if header and data:
        cols = separator.join(
            [str.ljust(str(col), width) for col, width in zip(rows[0], widths)]
        )
        print(cols)
    if data:
        for row in data:
            cols = separator.join(
                [str.ljust(str(col), width) for col, width in zip(row, widths)]
            )
            print(cols)
