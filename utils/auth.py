from functools import wraps

from flask import session, redirect, url_for, flash


def login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login"))

        return view_function(*args, **kwargs)

    return wrapped_view


def admin_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login"))

        if session.get("role") != "ADMIN":
            flash("You do not have permission to access this page.", "error")
            return redirect(url_for("home"))

        return view_function(*args, **kwargs)

    return wrapped_view