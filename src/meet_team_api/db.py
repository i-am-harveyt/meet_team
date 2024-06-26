"""This is to setup the MySQL Database"""

import os

import mysql.connector
from mysql.connector.abstracts import (MySQLConnectionAbstract,
                                       MySQLCursorAbstract)

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DATABASE")


def get_connection() -> MySQLConnectionAbstract:
    """Initialize the connection"""
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
    )
    return conn


def get_cursor(connection) -> MySQLCursorAbstract:
    """Get cursor from connection"""
    return connection.cursor(dictionary=True)
