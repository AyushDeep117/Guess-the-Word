from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    request,
)

from services.game_service import (
    create_game,
    get_game_for_user,
    get_guesses_for_game,
    submit_guess,
)

from utils.auth import login_required
from utils.word_evaluator import evaluate_guess


game_bp = Blueprint("game", __name__, url_prefix="/game")


@game_bp.route("/")
@login_required
def game_home():
    return render_template("game.html")


@game_bp.route("/start", methods=["POST"])
@login_required
def start_game():

    game_id, error = create_game(session["user_id"])

    if error == "daily_limit":
        flash(
            "You have already played 3 games today.",
            "error",
        )
        return redirect(url_for("game.game_home"))

    if error == "no_words":
        flash(
            "No words are available to start a game.",
            "error",
        )
        return redirect(url_for("game.game_home"))

    return redirect(
        url_for(
            "game.play_game",
            game_id=game_id,
        )
    )


@game_bp.route("/<int:game_id>")
@login_required
def play_game(game_id):

    game = get_game_for_user(
        game_id,
        session["user_id"],
    )

    if game is None:
        flash("Game not found.", "error")
        return redirect(url_for("game.game_home"))

    guesses = get_guesses_for_game(game_id)

    evaluations = []

    for stored_guess in guesses:
        evaluations.append(
            {
                "guess": stored_guess["guess"],
                "evaluation": evaluate_guess(
                    game["target_word"],
                    stored_guess["guess"],
                ),
            }
        )

    safe_game = {
        "id": game["id"],
        "user_id": game["user_id"],
        "status": game["status"],
        "guesses_used": game["guesses_used"],
        "started_at": game["started_at"],
        "completed_at": game["completed_at"],
    }

    return render_template(
        "game.html",
        game=safe_game,
        guesses=guesses,
        evaluations=evaluations,
    )

@game_bp.route("/<int:game_id>/guess", methods=["POST"])
@login_required
def make_guess(game_id):

    guess = request.form.get(
        "guess",
        "",
    ).strip().upper()

    result, error = submit_guess(
        game_id,
        session["user_id"],
        guess,
    )

    if error == "game_not_found":
        flash("Game not found.", "error")
        return redirect(url_for("game.game_home"))

    if error == "game_finished":
        flash(
            "This game has already finished.",
            "error",
        )
        return redirect(
            url_for(
                "game.play_game",
                game_id=game_id,
            )
        )

    if error == "guess_limit_reached":
        flash(
            "You have used all 5 guesses.",
            "error",
        )
        return redirect(
            url_for(
                "game.play_game",
                game_id=game_id,
            )
        )

    if result["status"] == "WON":
        flash(
            "Congratulations! You guessed the word!",
            "success",
        )

    elif result["status"] == "LOST":
        flash(
            "Better luck next time!",
            "error",
        )

    game = get_game_for_user(
        game_id,
        session["user_id"],
    )

    guesses = get_guesses_for_game(game_id)

    evaluations = []

    for stored_guess in guesses:

        evaluations.append(
            {
                "guess": stored_guess["guess"],
                "evaluation": evaluate_guess(
                    game["target_word"],
                    stored_guess["guess"],
                ),
            }
        )

    return render_template(
        "game.html",
        game=game,
        guesses=guesses,
        evaluations=evaluations,
    )