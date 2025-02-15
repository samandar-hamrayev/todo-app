import datetime
from datetime import timedelta, datetime
from random import randint


class AdminToken:
    def __init__(self, email: str, created_by: int):
        self.created_by = created_by
        self.email = email
        self.token = str(randint(1000, 9999))
        self.is_used = False
        self.expires_at = datetime.now() + timedelta(hours=24)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def display(self):
        return (f"Email: {self.email}\n"
                f"Token: {self.token}\n"
                f"Created By: {self.created_by}\n"
                f"Is Used: {self.is_used}\n"
                f"Expires At: {self.expires_at}")

    def __repr__(self):
        return f"AdminToken({self.email} | Token: {self.token} | Created By: {self.created_by} | Used: {self.is_used} | Expires: {self.expires_at})"
