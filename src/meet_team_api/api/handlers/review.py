"""This module is the handler for `review`"""

from fastapi import status, HTTPException
from fastapi.responses import JSONResponse

from ...db import get_connection, get_cursor
from ...models.user import UserId


def get_group_members_and_reviews(group_id: int, user_id: int) -> list:
    """
    Retrieves the group members and their reviews for a given group and user.

    Args:
        group_id (int): The ID of the group.
        user_id (int): The ID of the user.

    Returns:
        list: A list containing the group members and their reviews.
            Each member is represented as a tuple with the following fields:
                - id (int): The ID of the member.
                - name (str): The name of the member.
                - description (str): The description of the member.

            Each review is represented as a tuple with the following fields:
                - id (int): The ID of the review.
                - user_id (int): The ID of the user who wrote the review.
                - content (str): The content of the review.
                - create_at (datetime): The timestamp when the review was created.
                - name (str): The name of the user who wrote the review.

            The returned list is structured as follows:
            {
                "data": {
                    "members": [
                        {
                            "id": int,
                            "name": str,
                            "description": str
                        },
                        ...
                    ],
                    "reviews": [
                        {
                            "id": int,
                            "user_id": int,
                            "content": str,
                            "create_at": datetime,
                            "name": str
                        },
                        ...
                    ]
                }
            }
    """
    conn = get_connection()
    cursor = get_cursor(conn)


    # check if user is in the group
    cursor.execute(
        """
        SELECT EXISTS(
            SELECT * FROM group_member
            WHERE user_id = %s AND group_id = %s
        ) AS in_group
        """,
        (user_id, group_id),
    )
    if cursor.fetchone()["in_group"] == 0:
        cursor.close()
        conn.close()
        raise Exception("You're not in this group")

    # fetch members
    cursor.execute(
        """
    SELECT u.id, u.name, u.description
    FROM `user` u
    JOIN `group_member` gm ON u.id = gm.user_id
    WHERE gm.group_id = %s
    """,
        (group_id,),
    )
    members = cursor.fetchall()

    # fetch reviews
    cursor.execute(
        """
    SELECT r.id, r.user_id, r.content, r.rating, r.create_at, u.name
    FROM `review` r
    JOIN `user` u ON u.id = r.user_id
    WHERE r.group_id = %s AND r.reviewer_id = %s
    """,
        (group_id, user_id),
    )
    reviews = cursor.fetchall()

    cursor.close()
    conn.close()
    return {
        "data": {
            "members": members,
            "reviews": reviews,
        }
    }


async def upsert_review(
    group_id, reviewer_id, reviews: dict[UserId, str | float]
) -> dict:
    """
    Upsert a review for a group and user.

    Args:
        group_id (int): The ID of the group.
        user_id (int): The ID of the user.
        content (str): The content of the review.

    Returns:
        dict: The result message.
    """
    conn = get_connection()
    cursor = get_cursor(conn)

    print(group_id, reviewer_id, reviews)

    # upsert review
    cursor.executemany(
        """
    INSERT INTO `review` (group_id, reviewer_id, user_id, content, rating)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        content = VALUES(content),
        rating = VALUES(rating)
    """,
        [
            (
                group_id,
                reviewer_id,
                user_id,
                review["content"],
                (review["rating"] * 10) // 5 / 2,
            )
            for user_id, review in reviews.items()
        ],
    )

    cursor.close()
    conn.commit()
    conn.close()

    return {"data": {"message": "ok"}}


async def get_user_review(user_id: UserId):
    """
    Retrieves all reviews written to a specific user.

    Parameters:
        user_id (UserId): The ID of the user whose reviews are to be retrieved.

    Returns:
        JSONResponse or HTTPException: A JSONResponse containing the reviews written by the user. The JSONResponse has the following structure:
            {
                "data": {
                    "reviews": List[Tuple[int, int, str, float, str]]
                }
            }
            - reviews: A list of tuples representing the reviews. Each tuple contains the following elements:
                - int: The ID of the review.
                - int: The ID of the course associated with the review.
                - str: The content of the review.
                - float: The rating given for the course.
                - str: The name of the course.
        HTTPException: If an error occurs during the retrieval process.
    """
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            """
        SELECT r.id, r.content, r.rating, c.name AS course
        FROM `review` AS r
        JOIN `course` AS c ON r.group_id = c.id
        WHERE r.user_id = %s
        """,
            (user_id,),
        )

        reviews = cursor.fetchall()
        cursor.close()
        conn.close()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"data": {"reviews": reviews}},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
