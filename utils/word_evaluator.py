from collections import Counter


CORRECT = "CORRECT"
PRESENT = "PRESENT"
ABSENT = "ABSENT"


def evaluate_guess(target, guess):
    """
    Compare a 5-letter guess against the target word.

    Returns a list containing the status of each letter:
    CORRECT, PRESENT, or ABSENT.
    """

    target = target.upper()
    guess = guess.upper()

    if len(target) != 5 or len(guess) != 5:
        raise ValueError("Target and guess must both contain 5 letters.")

    result = [ABSENT] * 5

    remaining_letters = Counter()

    # Pass 1: exact-position matches
    for index in range(5):
        if guess[index] == target[index]:
            result[index] = CORRECT
        else:
            remaining_letters[target[index]] += 1

    # Pass 2: correct letter but wrong position
    for index in range(5):
        if result[index] == CORRECT:
            continue

        letter = guess[index]

        if remaining_letters[letter] > 0:
            result[index] = PRESENT
            remaining_letters[letter] -= 1

    return result