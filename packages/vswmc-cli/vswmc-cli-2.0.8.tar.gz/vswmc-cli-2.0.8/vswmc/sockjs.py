from __future__ import print_function

import json
import random
import threading
import uuid

import requests


class SockJSSession(threading.Thread):
    def __init__(self, vswmc_url, on_data, session=None):
        threading.Thread.__init__(self)
        self.session = session or requests.Session()
        self.vswmc_url = vswmc_url
        self.on_data = on_data

        self.daemon = True

        self._completed = threading.Event()

        self.server_id = str(random.randint(0, 1000))
        self.session_id = str(uuid.uuid4())

        url = "/".join(
            [vswmc_url, "eventbus", self.server_id, self.session_id, "xhr_streaming"]
        )
        self.stream = self.session.post(url, stream=True, timeout=None)

        self.start()

    def run(self):
        for line in self.stream.iter_lines():
            data = line.decode("utf-8")

            if data[0] == "o":  # open
                # print('Socket connected')
                pass
            elif data[0] == "c":  # close
                print("Disconnected")
                break
            elif data[0] == "h":  # heartbeat
                pass
            elif data[0] == "m":  # message
                json_obj = json.loads(data[1:])
                self.on_data(json_obj, self)
            elif data[0] == "a":  # array of messages
                for msg in json.loads(data[1:]):
                    json_obj = json.loads(msg)
                    self.on_data(json_obj, self)
            else:
                print("got unexpected line", data)

        self._completed.set()

    def disconnect(self):
        self._completed.set()

    def result(self):
        return self._wait_on_signal(self._completed)

    def _wait_on_signal(self, event):
        # Wait until the future is done. We do not use wait() without timeout
        # because on Python 2.x this does not generate ``KeyboardInterrupt``.
        # https://bugs.python.org/issue8844
        # The actual timeout value does not have any impact
        while not event.wait(timeout=10):
            pass  # tick

    def send(self, message):
        url = "/".join(
            [self.vswmc_url, "eventbus", self.server_id, self.session_id, "xhr_send"]
        )
        response = self.session.post(
            url,
            data=json.dumps([message]),
            headers={
                "Content-Type": "text/plain",
            },
        )
        return response.status_code in (200, 204)
