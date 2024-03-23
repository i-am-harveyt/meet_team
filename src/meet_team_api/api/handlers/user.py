"""This is the user handlers, for the user router"""

import traceback

from mysql.connector.cursor import MySQLCursor

from ...db import get_db


async def find_one(**kwargs):
    """To find out one user"""


async def register(account, password, name):
    """To add a new user in
    @returns id
    """
    conn = get_db()
    cur = conn.cursor()

    query = """
    INSERT INTO user (account, password, name)
    VALUES (%(account)s, %(password)s, %(name)s)
    """
    new_user = {"account": account, "password": password, "name": name}

    cur.execute(query, new_user)
    conn.commit()

    new_user_id = cur.lastrowid
    cur.close()
    conn.close()
    return new_user_id


async def login(account, password):
    """To login"""
    conn = get_db()
    cur = conn.cursor()

    query = """
    SELECT id, name FROM user
    WHERE account=%s AND password=%s
    """
    cur.execute(query, (account, password))
    ret = cur.fetchone()
    cur.close()
    conn.close()
    return ret
