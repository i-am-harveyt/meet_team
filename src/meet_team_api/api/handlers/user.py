"""This is the user handlers, for the user router"""

from ...db import get_connection, get_cursor
from ...models.user import UserId


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


async def find_info(user_id: UserId, is_self: bool) -> dict[str, str]:
    """This function is to fetching user info"""
    conn = get_connection()
    cur = get_cursor(conn)
    ret = {}
    query: str = """
    SELECT id, account, name, description
    FROM user WHERE id=%s
    """
    cur.execute(query, (user_id,))
    ret = cur.fetchone()
    cur.close()
    conn.close()
    return ret


async def fetch_course(user_id: UserId):
    conn = get_connection()
    cur = get_cursor(conn)
    ret = []

    cur.execute(
        """
        WITH joined_courses AS (
            SELECT * FROM `course_member` cm
            WHERE cm.user_id=%s
        )
        SELECT
            c.id,
            c.name,
            u.name AS teacher,
            c.year,
            c.semester
        FROM `course` c
        INNER JOIN
            `user` u
        ON
            c.owner_id = u.id
        INNER JOIN joined_courses jc ON c.id=jc.course_id
        """,
        (user_id,),
    )
    ret = cur.fetchall()

    cur.close()
    conn.close()
    return ret


async def fetch_tasks(user_id: UserId):
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute(
        """
        SELECT
            id,
            name,
            description,
            status
        FROM
            `task`
        WHERE
            assignee_id = %s
        """,
        (user_id,),
    )
    ret = cur.fetchall()

    cur.close()
    conn.close()
    return ret


async def update_info(user_id: UserId, description: str | None):
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute(
        """
        UPDATE `user` u
        SET description=%s
        WHERE u.id=%s
        """,
        (description, user_id),
    )
    conn.commit()

    cur.close()
    conn.close()
    return True
