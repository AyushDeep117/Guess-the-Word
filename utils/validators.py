import re


def validate_username(username):
    """
    Validate the username according to the project requirements.
    Username must contain at least 5 alphabetic characters.
    """

    if not username:
        return False, "Username is required."

    if len(username) < 5:
        return False, "Username must be at least 5 characters long."

    if not username.isalpha():
        return False, "Username must contain only letters."

    return True, ""

def validate_guess(guess):
    """
    Validate a player guess.

    Requirements:
    - Must be provided
    - Must contain exactly 5 characters
    - Must contain English alphabetic characters only
    """

    if not guess:
        return False, "Guess is required."

    guess = guess.strip()

    if len(guess) != 5:
        return False, "Guess must contain exactly 5 letters."

    if not re.fullmatch(r"[A-Za-z]{5}", guess):
        return False, "Guess must contain English letters only."

    return True, ""


def validate_password(password):
    """
    Validate the password according to the project requirements.

    Password must:
    - Be at least 5 characters long
    - Contain at least one alphabetic character
    - Contain at least one number
    - Contain at least one of $, %, *
    """

    if not password:
        return False, "Password is required."

    if len(password) < 5:
        return False, "Password must be at least 5 characters long."

    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    if not re.search(r"[$%*]", password):
        return False, "Password must contain at least one special character: $, %, or *."

    return True, ""