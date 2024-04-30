from typing import Optional

from mysql.connector.abstracts import (MySQLConnectionAbstract,
                                       MySQLCursorAbstract)

from ...db import get_connection, get_cursor


async def find(group_id: int, user_id: int, me: bool):
    conn = get_connection()
    cur = get_cursor(conn)

    # check if the user is in the group
    cur.execute(
        """
        SELECT EXISTS(
            SELECT * FROM group_member
            WHERE user_id = %s AND group_id = %s
        ) AS in_group
        """,
        (user_id, group_id),
    )
    if cur.fetchone()["in_group"] == False:
        cur.close()
        conn.close()
        raise Exception("You're not in this group")

    if me:
        query = """
        SELECT id, name, status FROM task
        WHERE group_id = %s AND %s IN (assignedd_id, reviewer_id)
        """
        cur.execute(query, (group_id, user_id))
    else:
        query = "SELECT id, name, status FROM task WHERE group_id = %s"
        cur.execute(query, (group_id,))
    ret = cur.fetchall()
    cur.close()
    conn.close()
    return ret


async def create(
    user_id: int,
    group_id: int,
    name: str,
    description: Optional[str],
    assignee_id: Optional[int],
    reviewer_id: Optional[int],
) -> int | None:
    conn: MySQLConnectionAbstract = get_connection()
    cur: MySQLCursorAbstract = get_cursor(conn)

    try:
        cur.execute(
            """
            INSERT INTO
                task (name, description, creator_id, assignee_id, reviewer_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (name, description, user_id, assignee_id, reviewer_id),
        )
        conn.commit()

        new_task_id: Optional[int] = cur.lastrowid
    except Exception as e:
        cur.close()
        conn.close()
        raise e

    cur.close()
    conn.close()
    return new_task_id
