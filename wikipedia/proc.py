#!/usr/bin/env python

import requests
import re
import sys
import time
import subprocess
from contextlib import contextmanager

ACCOUNT_ID_MATCHER = re.compile("Account ID: (.+)")
ACCOUNT_SECRET_MATCHER = re.compile("Account secret: (.+)")

@contextmanager
def server():
    """
    Context manager for running the server. This starts the server up, waits
    until its responsive, then yields. When the context manager's execution is
    resumed, it kills the server.
    """

    # Start the process
    server_proc = subprocess.Popen(["braid-server"], stdout=sys.stdout, stderr=sys.stderr)
    
    while True:
        # Check if the server is now responding to HTTP requests
        try:
            res = requests.get("http://localhost:8000", timeout=1)

            if res.status_code == 401:
                break
        except requests.exceptions.RequestException:
            pass

        # Server is not yet responding to HTTP requests - let's make sure it's
        # running in the first place
        if server_proc.poll() != None:
            raise Exception("Server failed to start")

        time.sleep(1)

    try:
        yield
    finally:
        server_proc.terminate()

def create_account():
    """Creates a braid account"""
    create_user_output = subprocess.check_output(["braid-account", "add"]).decode("utf-8")
    account_id = ACCOUNT_ID_MATCHER.search(create_user_output).groups()[0]
    secret = ACCOUNT_SECRET_MATCHER.search(create_user_output).groups()[0]
    return account_id, secret
