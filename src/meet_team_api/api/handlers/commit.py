from typing import Dict

from mysql.connector.abstracts import (MySQLConnectionAbstract,
                                       MySQLCursorAbstract)
from mysql.connector.types import RowItemType

from ...db import get_connection, get_cursor


async def find_all(user_id, group_id):
    conn: MySQLConnectionAbstract = get_connection()
    cur: MySQLCursorAbstract = get_cursor(conn)

    cur.execute(
        """
        SELECT EXISTS(
            SELECT * FROM group_member
            WHERE user_id = %s AND group_id = %s
        ) AS in_group
        """
    )

    exist = cur.fetchone()
    if not isinstance(exist, Dict[str, RowItemType]) or exist["in_group"] is False:
        cur.close()
        conn.close()
        raise Exception("You're not in this group")

    cur.execute(
        """
        SELECT
            task.id,
            task.name,
            task.create_at AS task_create,
            task.status,
            u.name AS user_name,
            c.create_at AS commit_create
        FROM
            task
        INNER JOIN `commit` c ON
            c.task_id = task.id
        INNER JOIN `user` u ON
            task.assignee_id = u.id
        WHERE task.group_id=%s
        """,
        (group_id,),
    )
    ret = cur.fetchall()

    cur.close()
    conn.close()

    return ret


async def create(user_id, task_id, description, reference_link):
    """This function is to create commits given `task_id`"""
    conn: MySQLConnectionAbstract = get_connection()
    cur: MySQLCursorAbstract = get_cursor(conn)

    cur.execute(
        """
        WITH task_with_group AS (
            SELECT t.* FROM `task` t 
            INNER JOIN `group` g ON t.group_id=g.id
            WHERE t.id=%s
        )
        SELECT EXISTS (
            SELECT * FROM task_with_group tg
            INNER JOIN group_member gm ON tg.group_id=gm.group_id
            WHERE gm.user_id=%s
        ) AS in_group
        """,
        (task_id, user_id),
    )

    exist = cur.fetchone()
    if exist is None or exist["in_group"] is False:
        cur.close()
        conn.close()
        raise Exception("You're not in this group")

    cur.execute(
        """
        INSERT INTO `commit` (task_id, creator_id, description, reference_link)
        VALUES (%s, %s, %s, %s)
        """,
        (task_id, user_id, description, reference_link),
    )
    new_commit_id = cur.lastrowid
    cur.execute(
        """
        UPDATE `task`
        SET status='Doing'
        WHERE id = %s
        """,
        (task_id,),
    )
    conn.commit()

    cur.close()
    conn.close()

    return new_commit_id
