from datetime import datetime
from enum import Enum


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
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def display(self):
        return (f"Title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Priority: {self.priority}\n"
                f"Due Date: {self.due_date}\n"
                f"Is completed: {self.is_completed}\n"
                f"Created at: {self.created_at}")
    def __repr__(self):
        return f"{self.title} | {self.priority} | {self.due_date}"
