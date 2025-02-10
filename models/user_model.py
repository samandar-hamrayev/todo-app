from datetime import datetime
from utils.user_utils import UserUtils


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.created_at = UserUtils.time_formatter(datetime.now())
        self.updated_at = UserUtils.time_formatter(datetime.now())
    
    