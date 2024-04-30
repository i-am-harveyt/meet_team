"""This module is the handler for `group`"""

from typing import Optional

from ...db import get_connection, get_cursor
from ...models.course import CourseId
from ...models.group import GroupId
from ...models.user import UserId


async def create(
    course_id: CourseId, owner_id: UserId, name: str, description: Optional[str]
):
    """This function is to create group, write into db"""
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute(
        """
        INSERT INTO `group`
        (course_id, owner_id, name, description)
        VALUES(%s, %s, %s, %s)
    """,
        (course_id, owner_id, name, description),
    )
    new_group_id = cur.lastrowid
    cur.execute(
        """
        INSERT INTO group_member (user_id, group_id)
        VALUES (%s, %s)
        """,
        (owner_id, new_group_id),
    )
    conn.commit()

    cur.close()
    conn.close()
    return new_group_id


async def find_one(group_id: GroupId):
    """This function finds a group's information given group_id"""
    conn = get_connection()
    cur = get_cursor(conn)

    cur.execute(
        """
    SELECT user.id, user.name, user.account
    FROM group_member gm
    INNER JOIN user ON gm.user_id=user.id
    WHERE gm.group_id=%s
    """,
        (group_id,),
    )
    members = cur.fetchall()

    cur.execute(
        """
        SELECT
            g.id,
            c.name AS course_name,
            u.name AS owner_name,
            g.name AS group_name,
            g.description
        FROM `group` g
        INNER JOIN user u ON g.owner_id=u.id
        INNER JOIN course c ON g.course_id=c.id
        WHERE g.id=%s
        """,
        (group_id,),
    )
    group = cur.fetchone()
    cur.close()
    conn.close()
    return {"group": group, "members": members}


async def update(
    user_id: UserId, group_id: GroupId, new_name: Optional[str], new_desc: Optional[str]
):
    """This function update the info of course"""
    conn = get_connection()
    cur = get_cursor(conn)

    has_name = isinstance(new_name, str)
    has_desc = isinstance(new_desc, str)

    query = f"""
    UPDATE `group` SET
    {"name = %s" if has_name else ""}
    {"," if has_name and has_desc else ""}
    {"description = %s" if has_desc else ""}
    WHERE id=%s AND owner_id=%s
    """
    params = (group_id, user_id)
    if isinstance(new_desc, str):
        params = (new_desc,) + params
    if isinstance(new_name, str):
        params = (new_name,) + params

    cur.execute(query, params)
    conn.commit()

    cur.close()
    conn.close()

    return group_id
