from typing import Text

from pony import orm

from database.db import db
from login_server import srp


class Account(db.Entity):
    name = orm.PrimaryKey(str)
    salt_str = orm.Required(str)
    verifier_str = orm.Required(str)
    session_key_str = orm.Optional(str)

    @property
    def salt(self) -> int:
        return int(self.salt_str)

    @property
    def verifier(self) -> int:
        return int(self.verifier_str)

    @property
    def session_key(self) -> int:
        return int(self.session_key_str)

    @classmethod
    def New(cls, username: Text, password: Text) -> 'Account':
        """Create a new Account and return it.

        This must be done inside a PonyORM session.

        Args:
            username: The username of the account.
            password: The password of the account.

        Returns:
            The newly created account.
        """
        salt = srp.Random(32)
        verifier = srp.GenerateVerifier(username.upper(), password, salt)
        return Account(
            name=username.upper(),
            salt_str=str(salt),
            verifier_str=str(verifier),
        )
