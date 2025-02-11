import psycopg2

from orm.config import db_info

from models.user_model import User


class UserDB:
    def __init__(self):
        self.conn = psycopg2.connect(**db_info)
        self.cur = self.conn.cursor()
        self.create_table() # darxol jadvalni yaratib qo'yamiz

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role VARCHAR(10) CHECK (role IN ('user', 'admin')),
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cur.execute(query)
        self.conn.commit()


    def add(self, user: User) -> tuple:
        query = """
        INSERT INTO users (username, email, role, password, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, username, email, role, created_at;
        """
        self.cur.execute(query, (user.username, user.email, user.role,  user.password, user.created_at, user.updated_at))
        self.conn.commit()
        return self.cur.fetchone()

    def get_by_id(self, user_id: int) -> tuple:
        query = """
        SELECT id, username, email, role, created_at, updated_at FROM users WHERE id = %s;
        """
        self.cur.execute(query, (user_id, ))
        return self.cur.fetchone()

    
    def get_all(self) -> list[tuple]:
        query = """
        SELECT id, username, email, role, created_at, updated_at FROM  users;
        """
        self.cur.execute(query)
        return self.cur.fetchall()


    def update(self, user_id, new_data):
        query = """
        UPDATE users SET username = %s, email = %s, role = %s, password = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s;
        """
        self.cur.execute(query, (new_data['username'], new_data['email'], new_data['role'], new_data['password'], user_id))
        self.conn.commit()


    def delete(self, user_id: int):
        query = """
        DELETE FROM users WHERE id = %s;
        """
        self.cur.execute(query, (user_id, ))
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

