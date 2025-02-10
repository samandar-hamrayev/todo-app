from datetime import datetime

class Todo:
    def __init__(self, 
                 user_id: int, 
                 title: str, 
                 description: str, 
                 priority: str, 
                 due_date: datetime, 
                 is_completed: bool = False
                 ):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.is_completed = is_completed