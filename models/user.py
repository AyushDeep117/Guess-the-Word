from datetime import datetime


class User:
    def __init__(
        self,
        username,
        password_hash,
        role="PLAYER",
        user_id=None,
        created_at=None,
    ):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at or datetime.now()