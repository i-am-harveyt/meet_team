"""This is the user handlers, for the user router"""

from ...db import get_connection, get_cursor
from ...models.user import UserId


async def register(account: str, password: str, name: str) -> int | None:
    """
    Register a new user in the database.

    Args:
        account (str): The user's account.
        password (str): The user's password.
        name (str): The user's name.

    Returns:
        int | None: The ID of the newly created user, or None if an error occurred.

    Raises:
        Exception: If an error occurs during the registration process.
    """
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
    """
    Asynchronously logs in a user given their account and password.

    Args:
        account (str): The user's account.
        password (str): The user's password.

    Returns:
        int | None: The ID of the user if they exist and their password matches, None otherwise.
    """
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
    """
    Asynchronously fetches the user information for a given user ID.

    Args:
        user_id (UserId): The ID of the user whose information is to be fetched.
        is_self (bool): Indicates whether the fetched information is for the current user.

    Returns:
        dict[str, str]: A dictionary containing the user information. The dictionary has the following keys:
            - 'id' (str): The ID of the user.
            - 'account' (str): The account of the user.
            - 'name' (str): The name of the user.
            - 'description' (str): The description of the user.
            If the user does not exist, an empty dictionary is returned.
    """
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
    """
    Asynchronously fetches the courses associated with a user.

    Args:
        user_id (UserId): The ID of the user whose courses are to be fetched.

    Returns:
        list: A list of tuples containing the course information. Each tuple contains the following elements:
            - int: The ID of the course.
            - str: The name of the course.
            - str: The name of the teacher associated with the course.
            - int: The year of the course.
            - str: The semester of the course.
    """
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
    """
    Asynchronously fetches the tasks associated with a user.

    Args:
        user_id (UserId): The ID of the user whose tasks are to be fetched.

    Returns:
        list: A list of tuples containing the task information. Each tuple contains the following elements:
            - int: The ID of the task.
            - str: The name of the task.
            - str: The description of the task.
            - str: The status of the task.
    """
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
    """
    Update the user information with the given user ID and description.

    Args:
        user_id (UserId): The ID of the user to update.
        description (str | None): The new description for the user. If None, the description will be set to None.

    Returns:
        bool: True if the user information was successfully updated, False otherwise.
    """
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
