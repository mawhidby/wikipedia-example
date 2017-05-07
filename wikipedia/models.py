import sqlite3
import os
import braid

# Location of the braid server
HOST_CONFIG = ("localhost", 8000)

# How long in seconds before braid a request times out
REQUEST_TIMEOUT = 600

def get_connection():
    return sqlite3.connect(os.environ["WIKIPEDIA_DATABASE_NAME"])

def get_client(cursor):
    account_id, account_secret = get_account_credentials(cursor)

    return braid.Client(
        HOST_CONFIG,
        account_id,
        account_secret,
        request_timeout=REQUEST_TIMEOUT,
        raise_on_error=True,
        scheme="http"
    )

def set_account_credentials(cursor, id, secret):
    cursor.execute("INSERT INTO accounts (id, secret) VALUES (?, ?)", (id, secret))

def get_account_credentials(cursor):
    cursor.execute("SELECT id, secret FROM accounts LIMIT 1")
    return cursor.fetchone()

def get_article_id(cursor, name):
    cursor.execute("SELECT id FROM articles WHERE name=?", (name,))
    results = cursor.fetchone()
    return results[0] if results else None

def get_article_name(cursor, id):
    cursor.execute("SELECT name FROM articles WHERE id=?", (id,))
    results = cursor.fetchone()
    return results[0] if results else None

def create_many_articles(cursor, args):
    cursor.executemany("INSERT INTO articles (name, id) VALUES (?, ?)", args)
