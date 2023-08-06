# Password credentials.

Store and query for username and password.

## Install
```shell
pip install --upgrade password-credentials==0.0.4
```

## Usage
```python

# Import Credentials class
from password_credentials.credentials import Credentials

# Initiliase with username and password.
credentials: Credentials = Credentials(username="USERNAME", password="PASSWORD")

# Generate credentials from enviroment values or if not defined prompt user.
credentials: Credentials = Credentials.get(
    service="EXAMPLE"
)
```