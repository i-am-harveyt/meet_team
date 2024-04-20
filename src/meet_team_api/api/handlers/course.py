"""This is the course handlers, for the course router"""

from typing import Optional

from ...db import get_connection, get_cursor


async def create_course(course_name, course_year, course_semester, owner_id) -> int:
    """To add a new user in"""
    conn = get_connection()
    cur = get_cursor(conn)

    query = """
    INSERT INTO course (name, year, semester, owner_id)
    VALUES (%s, %s, %s, %s)
    """
    cur.execute(query, (course_name, course_year, course_semester, owner_id))
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
    owner_id: int, course_id: int, new_name: str, new_desc: str
) -> Optional[int]:
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
    params = (course_id, owner_id)
    if isinstance(new_desc, str):
        params = (new_desc,) + params
    if isinstance(new_name, str):
        params = (new_name,) + params

    print(query)
    print(params)

    cur.execute(query, params)
    conn.commit()

    cur.close()
    conn.close()

    return id
