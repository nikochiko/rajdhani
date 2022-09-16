import sys

from rajdhani.app import app
from rajdhani import auth


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "add-user":
        auth.ensure_secret_key_file()
        name, email = sys.argv[2:4]
        auth.create_user(name, email)
    else:
        app.run()
