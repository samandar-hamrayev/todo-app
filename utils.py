from datetime import datetime

import bcrypt


class UserUtils:
    @staticmethod
    def time_formatter(current_time: datetime):
        return current_time.strftime("%Y-%m-%d  %H-%M-%S")

    @staticmethod
    def hash_password(password: str):
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        return hash



