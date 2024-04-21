"""This is the user handlers, for the user router"""

from ...db import get_connection, get_cursor


async def register(account: str, password: str, name: str) -> int | None:
    """To add a new user in"""
    conn = get_connection()
    cur = get_cursor(conn)

    query = """
    INSERT INTO user (account, password, name)
    VALUES (%(account)s, %(password)s, %(name)s)
    """
    new_user = {"account": account, "password": password, "name": name}

    try:
        cur.execute(query, new_user)
        conn.commit()
    except Exception as e:
        raise e

    new_user_id = cur.lastrowid
    cur.close()
    conn.close()
    return new_user_id


async def login(account: str, password: str) -> int | None:
    """To login"""
    conn = get_connection()
    cur = get_cursor(conn)

    query = """
    SELECT id FROM user
    WHERE account=%s AND password=%s
    """
    cur.execute(query, (account, password))
    ret = cur.fetchone()
    cur.close()
    conn.close()
    return ret


async def find_info(user_id: int, is_self: bool) -> dict[str, str]:
    """This function is to fetching user info"""
    conn = get_connection()
    cur = get_cursor(conn)
    if is_self:
        query: str = """
        SELECT id, account, name, description
        FROM user WHERE id=%s
        """
        cur.execute(query, (user_id,))
        ret = cur.fetchone()
        cur.close()
        conn.close()
        return ret
    return {}
