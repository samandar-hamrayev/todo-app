from datetime import datetime

from utils import UserUtils


class User:
    def __init__(self, username: str, email: str, role: str, password: str,):
        self.username = username
        self.email = email
        self.password = UserUtils.hash_password(password)
        self.role = role
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def display(self):
        return (f"Username: {self.username}\n"
                f"Email: {self.email}\n"
                f"Creating at: {UserUtils.time_formatter(str(self.created_at))}")
    def __repr__(self):
        return f"{self.username} || {self.updated_at}"
    