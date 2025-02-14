import psycopg2
from orm.config import db_info
from datetime import datetime
from models.todo_model import Todo

class TodoDB:
    def __init__(self):
        self.conn = psycopg2.connect(**db_info)
        self.cur = self.conn.cursor()

        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT CHECK (priority IN ('low', 'medium', 'high')),
            due_date TIMESTAMP,
            is_completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cur.execute(query)
        self.conn.commit()

    def add(self, todo: Todo) -> tuple:
        query = """
        INSERT INTO todos (user_id, title, description, priority, due_date, is_completed, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """
        self.cur.execute(
            query,
            (
                todo.user_id,
                todo.title,
                todo.description,
                todo.priority,
                todo.due_date,
                todo.is_completed,
                todo.created_at,
                todo.updated_at,
            ),
        )
        self.conn.commit()
        return self.cur.fetchone()  # Yangi todo ID ni qaytaradi


    def get_by_id(self, todo_id: int) -> tuple:
        query = "SELECT * FROM todos WHERE id = %s;"
        self.cur.execute(query, (todo_id,))
        return self.cur.fetchone()


    def get_by_user_id(self, user_id):
        query = """SELECT * FROM todos WHERE user_id = %s;"""
        self.cur.execute(query, (user_id, ))
        return self.cur.fetchall()

    def get_by_title_from_user(self, user_id, title):
        query = """SELECT * FROM todos WHERE user_id = %s AND title =%s;"""
        self.cur.execute(query, (user_id, title))
        return self.cur.fetchone()


    def get_all(self) -> list[tuple]:
        query = "SELECT * FROM todos;"
        self.cur.execute(query)
        return self.cur.fetchall()


    def update(self, user_id, new_data):
        set_clause = ", ".join([f"{key} = %s" for key in new_data.keys()])
        values = list(new_data.values()) + [user_id]

        query = f"""
        UPDATE todos 
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s;
        """
        self.cur.execute(query, values)
        self.conn.commit()


    def delete(self, todo_id: int):
        query = "DELETE FROM todos WHERE id = %s;"
        self.cur.execute(query, (todo_id,))
        self.conn.commit()


    def close(self):
        self.cur.close()
        self.conn.close()




