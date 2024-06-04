from ...db import get_connection, get_cursor
from ...models.user import UserId
from ...models.group import GroupId


def user_in_group(user_id: UserId, group_id: GroupId):
    """This function is to check if a user is in a group"""
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
    if cur.fetchone()["in_group"] == 0:
        cur.close()
        conn.close()
        raise Exception("You're not in this group")
    return True