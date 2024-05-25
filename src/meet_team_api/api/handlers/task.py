from typing import Optional

from mysql.connector.abstracts import (MySQLConnectionAbstract,
                                       MySQLCursorAbstract)

from ...db import get_connection, get_cursor
from ...models.user import UserId


async def find_all(group_id: int, user_id: int, me: bool):
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
    if cur.fetchone()["in_group"] is False:
        cur.close()
        conn.close()
        raise Exception("You're not in this group")

    if me:
        query = """
        SELECT
            id,
            name,
            task.description,
            status
        FROM
            task
        WHERE
            group_id = %s
            AND
            %s IN (assignedd_id, reviewer_id)
        """
        cur.execute(query, (group_id, user_id))
    else:
        query = """
        SELECT
            id,
            name,
            description,
            status
        FROM
            task
        WHERE
            group_id = %s
            """
        cur.execute(query, (group_id,))
    ret = cur.fetchall()
    cur.close()
    conn.close()
    return ret


async def find_one(task_id: int, user_id):
    conn = get_connection()
    cur = get_cursor(conn)

    # check if the user is in the group
    cur.execute(
        """
        SELECT EXISTS(
            SELECT *
            FROM `group_member` gm
            INNER JOIN `task` t
            ON t.group_id = gm.group_id
            WHERE user_id=%s AND t.id=%s
        ) AS in_group;
        """,
        (user_id, task_id),
    )
    result = cur.fetchone()
    if result["in_group"] is False:
        cur.close()
        conn.close()
        raise Exception("You're not in this group")

    cur.execute(
        """
        SELECT
            task.id,
            task.name,
            task.description,
            assignee_id,
            u1.name AS assignee_name,
            reviewer_id,
            u2.name AS reviewer_name,
            task.create_at,
            task.close_at,
            task.status
        FROM task
        LEFT JOIN `user` u1 ON u1.id=assignee_id
        LEFT JOIN `user` u2 ON u2.id=reviewer_id
        WHERE task.id=%s
        """,
        (task_id,),
    )
    task_info = cur.fetchone()
    if task_info["create_at"] is not None:
        task_info["create_at"] = task_info["create_at"].isoformat()
    if task_info["close_at"] is not None:
        task_info["close_at"] = task_info["close_at"].isoformat()
    if task_info.get("assignee_id", None) is not None:
        task_info["assignee"] = {
            "id": task_info["assignee_id"],
            "name": task_info["assignee_name"],
        }
        del task_info["assignee_id"]
        del task_info["assignee_name"]
    else:
        task_info["assignee"] = {
            "id": None,
            "name": None,
        }
    if task_info.get("reviewer_id", None) is not None:
        task_info["reviewer"] = {
            "id": task_info["reviewer_id"],
            "name": task_info["reviewer_name"],
        }
        del task_info["reviewer_id"]
        del task_info["reviewer_name"]
    else:
        task_info["reviewer"] = {
            "id": None,
            "name": None,
        }

    cur.execute(
        """
        WITH c AS (
            SELECT *
            FROM `commit`
            WHERE task_id=%s
        )
        SELECT
            c.id,
            c.creator_id,
            u.name AS username,
            c.title,
            c.description,
            c.reference_link,
            c.create_at
        FROM c
        INNER JOIN `user` u
        ON c.creator_id=u.id;
        """,
        (task_id,),
    )
    commit_info = cur.fetchall()
    for cmt in commit_info:
        cmt["create_at"] = cmt["create_at"].isoformat()
    cur.close()
    conn.close()
    return {"task": task_info, "commits": commit_info}


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
                task (
                    name,
                    description,
                    group_id,
                    creator_id,
                    assignee_id,
                    reviewer_id
                )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (name, description, group_id, user_id, assignee_id, reviewer_id),
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


async def patch(user_id: UserId, task_id: int):
    conn = get_connection()
    cur = get_cursor(conn)
    # check if the user is in the group
    cur.execute(
        """
        SELECT EXISTS(
            SELECT *
            FROM `group_member` gm
            INNER JOIN `task` t
            ON t.group_id = gm.group_id
            WHERE user_id=%s AND t.id=%s
        ) AS in_group;
        """,
        (user_id, task_id),
    )
    result = cur.fetchone()
    if result["in_group"] is False:
        cur.close()
        conn.close()
        raise Exception("You're not in this group")

    cur.execute(
        """
        UPDATE `task` SET status='Done'
        WHERE id = %s
        """,
        (task_id,),
    )
    conn.commit()

    cur.close()
    conn.close()
