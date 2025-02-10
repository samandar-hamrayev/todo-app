
from models.user_model import User

class UserDB:
    @staticmethod
    def add(user: User) -> tuple:
        pass

    @staticmethod
    def get_by_id(user_id: int) -> tuple:
        pass
    
    @staticmethod
    def get_all() -> list[tuple]:
        """
        superuserlar uchun ishlaydi
        """
        pass

    @staticmethod
    def update(user_id, new_data):
        pass