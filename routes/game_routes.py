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

    return render_template(
        "game.html",
        game=game,
        guesses=guesses,
    )


@game_bp.route("/<int:game_id>/guess", methods=["POST"])
@login_required
def make_guess(game_id):
    guess = request.form.get("guess", "").strip().upper()

    guess_number, result = submit_guess(
        game_id,
        session["user_id"],
        guess,
    )

    if result == "WON":
        flash("Congratulations! You guessed the word!", "success")
    elif result == "LOST":
        flash("Better luck next time!", "error")
    elif result == "game_not_found":
        flash("Game not found.", "error")
    elif result == "game_finished":
        flash("This game has already finished.", "error")
    elif result == "guess_limit_reached":
        flash("You have used all 5 guesses.", "error")
        
    return redirect(
        url_for(
            "game.play_game",
            game_id=game_id,
        )
    )