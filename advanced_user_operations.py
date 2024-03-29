import sqlite3

conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()

create_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    address TEXT
);
"""

cursor.execute(create_table_sql)

conn.commit()
conn.close()


class AdvancedUserOperations:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

    def create_user_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    address TEXT
                )
            ''')
            self.conn.commit()
            print("User table created successfully.")
        except sqlite3.Error as e:
            print("Error creating user table:", e)

    def create_user_with_profile(self, name, email, password, age=None, gender=None, address=None):
        try:
            self.cursor.execute('''
                INSERT INTO users (username, email, password, age, gender, address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, email, password, age, gender, address))
            self.conn.commit()
            print("User created successfully.")
        except sqlite3.Error as e:
            print("Error creating user:", e)

    def retrieve_user_by_email(self, email):
        try:
            self.cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = self.cursor.fetchone()
            if user:
                print("User retrieved successfully:", user)
                return user
            else:
                print("User with email {} not found.".format(email))
                return None
        except sqlite3.Error as e:
            print("Error retrieving user:", e)
            return None

    def retrieve_users_by_criteria(self, min_age=None, max_age=None, gender=None):
        try:
            query = 'SELECT * FROM users WHERE 1'
            if min_age:
                query += f' AND age >= {min_age}'
            if max_age:
                query += f' AND age <= {max_age}'
            if gender:
                query += f' AND gender = "{gender}"'
            self.cursor.execute(query)
            users = self.cursor.fetchall()
            print("Users retrieved successfully:", users)
            return users
        except sqlite3.Error as e:
            print("Error retrieving users:", e)
            return []

    def update_user_profile(self, email, age=None, gender=None, address=None):
        try:
            updates = []
            if age:
                updates.append(f'age = {age}')
            if gender:
                updates.append(f'gender = "{gender}"')
            if address:
                updates.append(f'address = "{address}"')

            if updates:
                update_str = ', '.join(updates)
                self.cursor.execute(f'UPDATE users SET {update_str} WHERE email = "{email}"')
                self.conn.commit()
                print("User profile updated successfully.")
            else:
                print("No updates provided.")
        except sqlite3.Error as e:
            print("Error updating user profile:", e)

    def delete_users_by_criteria(self, gender=None):
        try:
            if gender:
                self.cursor.execute(f'DELETE FROM users WHERE gender = "{gender}"')
            else:
                self.cursor.execute('DELETE FROM users')
            self.conn.commit()
            print("Users deleted successfully.")
        except sqlite3.Error as e:
            print("Error deleting users:", e)

    def __del__(self):
        self.conn.close()
