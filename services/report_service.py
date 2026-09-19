from database.db import get_connection


def get_daily_report(report_date):
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                COUNT(DISTINCT user_id) AS users,
                COUNT(
                    CASE
                        WHEN status = 'WON'
                        THEN 1
                    END
                ) AS correct_guesses
            FROM games
            WHERE DATE(started_at, 'localtime') = ?
            """,
            (report_date,),
        ).fetchone()

        return {
            "date": report_date,
            "users": row["users"],
            "correct_guesses": row["correct_guesses"],
        }

    finally:
        connection.close()

def get_user_report(user_id):
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                DATE(started_at, 'localtime') AS game_date,
                COUNT(*) AS words_tried,
                COUNT(
                    CASE
                        WHEN status = 'WON'
                        THEN 1
                    END
                ) AS correct_guesses
            FROM games
            WHERE user_id = ?
            GROUP BY DATE(started_at, 'localtime')
            ORDER BY game_date DESC
            """,
            (user_id,),
        ).fetchall()

        return rows

    finally:
        connection.close()

def get_all_users():
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT id, username
            FROM users
            ORDER BY username
            """
        ).fetchall()

        return rows

    finally:
        connection.close()