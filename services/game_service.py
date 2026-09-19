import random
from utils.word_evaluator import evaluate_guess
from database.db import get_connection


MAX_DAILY_GAMES = 3
MAX_GUESSES = 5



def count_games_today(user_id):
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT COUNT(*) AS game_count
            FROM games
            WHERE user_id = ?
            AND DATE(started_at) = DATE('now', 'localtime')
            """,
            (user_id,),
        ).fetchone()

        return row["game_count"]

    finally:
        connection.close()

def can_start_game(user_id):
    games_today = count_games_today(user_id)

    return games_today < MAX_DAILY_GAMES


def get_random_word():
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT id, word
            FROM words
            ORDER BY RANDOM()
            LIMIT 1
            """
        ).fetchone()

        return row

    finally:
        connection.close()

def create_game(user_id):
    if not can_start_game(user_id):
        return None, "daily_limit"

    word = get_random_word()

    if word is None:
        return None, "no_words"

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO games (
                user_id,
                word_id,
                status,
                guesses_used
            )
            VALUES (?, ?, 'ACTIVE', 0)
            """,
            (user_id, word["id"]),
        )

        connection.commit()

        return cursor.lastrowid, None

    finally:
        connection.close()

def get_game_for_user(game_id, user_id):
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                games.id,
                games.user_id,
                games.word_id,
                games.status,
                games.guesses_used,
                games.started_at,
                games.completed_at,
                words.word AS target_word
            FROM games
            JOIN words
                ON games.word_id = words.id
            WHERE games.id = ?
            AND games.user_id = ?
            """,
            (game_id, user_id),
        ).fetchone()

        return row

    finally:
        connection.close()

def get_guesses_for_game(game_id):
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                game_id,
                guess,
                guess_number,
                guessed_at
            FROM guesses
            WHERE game_id = ?
            ORDER BY guess_number
            """,
            (game_id,),
        ).fetchall()

        return rows

    finally:
        connection.close()

def submit_guess(game_id, user_id, guess):

    game = get_game_for_user(
        game_id,
        user_id,
    )

    if game is None:
        return None, "game_not_found"

    if game["status"] != "ACTIVE":
        return None, "game_finished"

    if game["guesses_used"] >= MAX_GUESSES:
        return None, "guess_limit_reached"

    next_guess_number = game["guesses_used"] + 1

    evaluation = evaluate_guess(
        game["target_word"],
        guess,
    )

    if guess == game["target_word"]:
        new_status = "WON"

    elif next_guess_number == MAX_GUESSES:
        new_status = "LOST"

    else:
        new_status = "ACTIVE"

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO guesses (
                game_id,
                guess,
                guess_number
            )
            VALUES (?, ?, ?)
            """,
            (
                game_id,
                guess,
                next_guess_number,
            ),
        )

        if new_status == "ACTIVE":

            connection.execute(
                """
                UPDATE games
                SET guesses_used = ?
                WHERE id = ?
                """,
                (
                    next_guess_number,
                    game_id,
                ),
            )

        else:

            connection.execute(
                """
                UPDATE games
                SET
                    guesses_used = ?,
                    status = ?,
                    completed_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    next_guess_number,
                    new_status,
                    game_id,
                ),
            )

        connection.commit()

        return {
            "guess_number": next_guess_number,
            "evaluation": evaluation,
            "status": new_status,
        }, None

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()