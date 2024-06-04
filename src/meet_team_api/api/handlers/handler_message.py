# create 新的message
from typing import Dict

from mysql.connector.abstracts import (MySQLConnectionAbstract,
                                       MySQLCursorAbstract)
from mysql.connector.types import RowItemType

from ...db import get_connection, get_cursor

async def find_all(creator_id,task_id):
    conn: MySQLConnectionAbstract = get_connection()
    cur: MySQLCursorAbstract = get_cursor(conn)

    cur.execute(
        """
        SELECT EXISTS(
            SELECT * FROM task
            WHERE user_id = %s AND task_id = %s
        ) AS in_task
        """
    )

    exist = cur.fetchone()
    if not isinstance(exist, Dict[str, RowItemType]) or exist["in_task"] is False:
        cur.close()
        conn.close()
        raise Exception("You're not in this group")

    cur.execute(
        """
        SELECT
            message.id,
            message.description
            message.create_at AS message_create,
            u.name AS user_name,
        FROM
            message
        INNER JOIN user u ON
            message.creator_id = u.id
        WHERE message.task_id=%s
        """,
        (task_id,),
    )
    ret = cur.fetchall()

    cur.close()
    conn.close()

    return ret


async def create(task_id, creator_id, description):
    """This function is to create a new message """
    conn: MySQLConnectionAbstract = get_connection()
    cur: MySQLCursorAbstract = get_cursor(conn)
    cur.execute(
        """ 
        INSERT INTO `message` (task_id, creator_id, description)
        VALUES (%s, %s, %s)
        """, 
        (task_id, creator_id, description),
    )
    conn.commit()

    cur.close()
    conn.close()
