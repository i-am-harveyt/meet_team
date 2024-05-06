"""This is the course handlers, for the course router"""

from typing import Optional

from ...db import get_connection, get_cursor
from ...models.course import CourseId


async def join(course_id: int, user_id: int):
    """To add a user into the `course_user` table"""
    conn = get_connection()
    cur = get_cursor(conn)

    query = """
    INSERT INTO course_member (course_id, user_id)
    VALUES (%s, %s)
    """
    try:
        cur.execute(query, (course_id, user_id))
        conn.commit()
    except Exception as e:
        cur.close()
        conn.close()
        raise e
    cur.close()
    conn.close()
    return True


async def create_course(
    course_name, course_year, course_semester, owner_id
) -> CourseId:
    """To add a new user in"""
    conn = get_connection()
    cur = get_cursor(conn)

    course_query = """
    INSERT INTO course (name, year, semester, owner_id)
    VALUES (%s, %s, %s, %s)
    """
    cur.execute(course_query, (course_name, course_year, course_semester, owner_id))
    course_id = cur.lastrowid

    member_query = """
    INSERT INTO course_member (course_id, user_id, role)
    VALUES (%s, %s, %s)
    """
    cur.execute(member_query, (course_id, owner_id, "Prof"))
    conn.commit()

    new_course_id = cur.lastrowid
    cur.close()
    conn.close()
    return new_course_id


async def find_course(course_id: int) -> Optional[dict[str, int | str]]:
    """This function returns the course info given `course_id`"""
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute(
        """
        SELECT id, name, year, semester, description
        FROM course
        WHERE id = %s
        """,
        (course_id,),
    )

    ret: dict[str, int | str] = cur.fetchone()

    cur.close()
    conn.close()

    return ret


async def update_course(
    user_id: int, course_id: int, new_name: str | None, new_desc: str | None
) -> int:
    """This function update the info of course"""
    conn = get_connection()
    cur = get_cursor(conn)

    has_name = isinstance(new_name, str)
    has_desc = isinstance(new_desc, str)

    query = f"""
    UPDATE course SET
    {"name = %s" if has_name else ""}
    {"," if has_name and has_desc else ""}
    {"description = %s" if has_desc else ""}
    WHERE id=%s AND owner_id=%s
    """
    params = (course_id, user_id)
    if isinstance(new_desc, str):
        params = (new_desc,) + params
    if isinstance(new_name, str):
        params = (new_name,) + params

    cur.execute(query, params)
    conn.commit()

    cur.close()
    conn.close()

    return course_id
