class Game:
    def __init__(
        self,
        game_id,
        user_id,
        word_id,
        status,
        guesses_used,
        started_at,
        completed_at=None,
    ):
        self.id = game_id
        self.user_id = user_id
        self.word_id = word_id
        self.status = status
        self.guesses_used = guesses_used
        self.started_at = started_at
        self.completed_at = completed_at