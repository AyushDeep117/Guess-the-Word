PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL UNIQUE,

    password_hash TEXT NOT NULL,

    role TEXT NOT NULL DEFAULT 'PLAYER'
        CHECK (role IN ('PLAYER', 'ADMIN')),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    word TEXT NOT NULL UNIQUE,

    CHECK (length(word) = 5),

    CHECK (word = upper(word))
);


CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    word_id INTEGER NOT NULL,

    status TEXT NOT NULL DEFAULT 'ACTIVE'
        CHECK (status IN ('ACTIVE', 'WON', 'LOST')),

    guesses_used INTEGER NOT NULL DEFAULT 0
        CHECK (guesses_used BETWEEN 0 AND 5),

    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    completed_at TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id),

    FOREIGN KEY (word_id)
        REFERENCES words(id)
);


CREATE TABLE IF NOT EXISTS guesses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    game_id INTEGER NOT NULL,

    guess TEXT NOT NULL,

    guess_number INTEGER NOT NULL
        CHECK (guess_number BETWEEN 1 AND 5),

    guessed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (game_id)
        REFERENCES games(id)
        ON DELETE CASCADE,

    UNIQUE (game_id, guess_number),

    CHECK (length(guess) = 5),

    CHECK (guess = upper(guess))
);

CREATE INDEX IF NOT EXISTS idx_games_user_started
ON games(user_id, started_at);