# Typing.
from __future__ import annotations
from typing import Union

# Getting password.
from getpass import getpass

# Gettng enviroment values.
from os import getenv


class Credentials:
    """For storing credentials."""

    username: str
    password: str

    def __init__(self, username: str, password: str) -> Credentials:
        """Initialize credentials.

        Args:
            username (str): Username
            password (str): Password

        Returns:
            Credentials: Itself.
        """
        self.username = username
        self.password = password

    @classmethod
    def get(cls, service: str) -> Credentials:
        """Get credentials.

        Args:
            service (str): Service/ENV name.

        Returns:
            Credentials: Gotten credentials.
        """

        # Get from env.
        username: Union[str, None] = getenv(
            "{service}_USERNAME".format(service=service)
        )
        password: Union[str, None] = getenv(
            "{service}_PASSWORD".format(service=service)
        )
        # Get from input.
        if not username or not password:
            print("Enter {service} credentials:".format(service=service))
        return cls(
            username=username or input("Username:"), password=password or getpass()
        )
