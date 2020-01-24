from typing import Text


class Account:
    @classmethod
    def Key(cls, name: Text) -> Text:
        return f'account::{name.upper()}'

    def __init__(self, name: Text, salt: int, verifier: int):
        self.name = name.upper()
        self.salt = salt
        self.verifier = verifier
