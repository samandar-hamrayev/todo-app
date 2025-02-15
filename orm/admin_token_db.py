import psycopg2
from models.admin_token import AdminToken

from orm.config import db_info


class AdminTokenDB:
    def __init__(self):
        self.conn = psycopg2.connect(**db_info)
        self.cur = self.conn.cursor()

        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS admin_tokens (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            token VARCHAR(4) NOT NULL,
            created_by INTEGER REFERENCES users(id) ON DELETE CASCADE,
            is_used BOOLEAN DEFAULT FALSE,
            expires_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP + INTERVAL '24 hours',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        self.cur.execute(query)
        self.conn.commit()

    def add(self, admin_token: AdminToken):
        query = """
        INSERT INTO admin_tokens (email, token, created_by, is_used, expires_at, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *;
        """
        self.cur.execute(
            query,
            (
                admin_token.email,
                admin_token.token,
                admin_token.created_by,
                admin_token.is_used,
                admin_token.expires_at,
                admin_token.created_at,
                admin_token.updated_at
            ),
        )
        self.conn.commit()
        return self.cur.fetchone()


    def get_all(self):
        query = """
        SELECT adt.email, adt.token, u.username as created_by adt.is_used, adt.expires_at, adt.created_by, adt.updated_at
        FROM admin_tokens adt
        JOIN users u ON u.id == adt.created_by.
        ORDER BY adt.is_used ASC AND adt.expires_at;
        """
        self.cur.execute(query)
        return self.cur.fetchall()

    def update_admin_token(self, admin_token_id, new_data: dict):
        set_clause = ", ".join([f"{key} = %s" for key in new_data.keys()])
        values = list(new_data.values()) + [admin_token_id]

        query = f"""
        UPDATE admin_tokens 
        SET {set_clause}, updated_at = CURRENT_TIMESTAMP 
        WHERE id = %s; """
        self.cur.execute(query, values)
        self.conn.commit()


    def get_by_id(self, admin_token_id):
        query = """
        SELECT * FROM admin_tokens WHERE id = %s"""
        self.cur.execute(query, (admin_token_id, ))
        return self.cur.fetchone()

    def get_by_creator_id(self, user_id):
        query = """
            SELECT * FROM admin_tokens WHERE created_by = %s;
        """
        self.cur.execute(query, (user_id, ))
        return self.cur.fetchall()

    def delete_by_id(self, admin_token_id):
        query = """
        DELETE FROM admin_tokens WHERE id = %s;
        """
        self.cur.execute(query, (admin_token_id, ))
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()






