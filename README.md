# Guess The Word

## Overview

Guess The Word is a Flask-based word guessing game with
player and administrator roles.

Players can register, log in, start games, and attempt to
guess a randomly selected five-letter word. Administrators
can access reports containing game and user statistics.

## Features

- User registration and login
- Password and username validation
- Role-based access control
- Player dashboard
- Word guessing game
- Wordle-style guess evaluation
- Correct, present, and absent letter feedback
- Maximum 5 guesses per game
- Maximum 3 games per user per day
- Previous guesses displayed in sequence
- Game status tracking
- Admin dashboard
- Daily administrative report
- Per-user administrative report
- SQLite database
- Session-based authentication
- Input validation
- Unit tests

## Game Rules

1. A random five-letter word is selected from the database
   when a new game starts.
2. The player can make a maximum of 5 guesses.
3. Each guess must contain exactly 5 English letters.
4. A correct letter in the correct position is shown as green.
5. A correct letter in the wrong position is shown as orange.
6. A letter that does not occur in the target word is shown as grey.
7. If the player guesses the word correctly, the game is won.
8. If all 5 guesses are used without finding the word, the
   game is lost.
9. A player can start a maximum of 3 games per day.

## User Validation Rules

### Username

- Must be provided.
- Must contain at least 5 characters.
- Must contain letters only.

### Password

- Must be provided.
- Must contain at least 5 characters.
- Must contain at least one alphabetic character.
- Must contain at least one number.
- Must contain at least one of the following special characters:
  `$`, `%`, `*`.

### Guess

- Must be provided.
- Must contain exactly 5 letters.
- Must contain English alphabetic characters only.

## Roles

### Player

A player can:

- Register an account.
- Log in.
- Access the player dashboard.
- Start a game.
- Submit guesses.
- View previous guesses and their results.
- Play up to 3 games per day.

### Administrator

An administrator can:

- Log in through the same authentication system.
- Access the administrator dashboard.
- View the daily report.
- View reports for individual users.

## Reports

### Daily Report

The daily report provides:

- Number of users who played on the selected date.
- Number of correct guesses/games for that date.

### User Report

The user report provides:

- Date of play.
- Number of words/games tried.
- Number of correct guesses/games.

## Technologies

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Python `unittest`

## Project Structure

```text
Guess the Word/
│
├── database/
│   ├── db.py
│   └── ...
│
├── routes/
│   ├── auth_routes.py
│   ├── game_routes.py
│   └── admin_routes.py
│
├── services/
│   ├── game_service.py
│   └── ...
│
├── utils/
│   ├── auth.py
│   ├── validators.py
│   └── word_evaluator.py
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── admin_dashboard.html
│   ├── game.html
│   ├── daily_report.html
│   └── user_report.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── game.js
│
├── tests/
│   ├── test_game_service.py
│   ├── test_validators.py
│   └── test_word_evaluator.py
│
├── app.py
├── requirements.txt
├── README.md
└── guess_the_word.db