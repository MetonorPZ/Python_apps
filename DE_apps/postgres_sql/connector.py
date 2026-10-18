import os

import pyodbc


def connect() -> pyodbc.Connection:
    driver = os.environ.get("PG_ODBC_DRIVER", "PostgreSQL Unicode(x64)")
    server = os.environ.get("PGHOST", "127.0.0.1")
    port = os.environ.get("PGPORT", "5431")
    database = os.environ.get("PGDATABASE", "stock_data")
    username = os.environ["PGUSER"]
    password = os.environ["PGPASSWORD"]

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"PORT={port};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )
    return pyodbc.connect(connection_string)
