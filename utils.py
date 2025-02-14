import re
from datetime import datetime

import bcrypt

class UserUtils:
    @staticmethod
    def time_formatter(current_time):
        formatted_time = datetime.strptime(
            current_time,
            "%Y-%m-%d %H:%M:%S.%f"
        ).strftime("%Y-%m-%d %H-%M-%S")

        return formatted_time

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_pwd.decode('utf-8')
    

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def email_validator(email) -> bool:
        pattern = "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"
        valid = re.match(pattern, email)
        return True if valid else False

    @staticmethod
    def username_validator(username: str) -> bool:
        pattern = "^[a-z0-9_-]{3,15}$"
        valid = re.match(pattern, username)
        return True if valid else False

    @staticmethod
    def password_validator(password: str) -> bool:
        pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{4,}$"
        valid = re.match(pattern, password)
        return True if valid else False







