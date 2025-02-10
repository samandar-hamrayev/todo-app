from datetime import datetime

class UserUtils:
    @staticmethod
    def time_formatter(current_time: datetime):
        return current_time.strftime("%Y-%m-%d-%H-%M-%S")

    @staticmethod
    def hash_password(password: str):
        pass