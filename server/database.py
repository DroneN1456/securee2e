import sqlite3

conn = ''

cursor = ''


def delete_users():
    global cursor
    cursor.execute(
        """
        DELETE FROM users;
        """
    )
    save_changes()


def create_user(name, password):
    global cursor
    cursor.execute(
        f"""
        INSERT INTO users(username, password) VALUES("{name}", "{password}")
        """
    )
    save_changes()


def check_password(user, password):
    global cursor
    cursor.execute(
        f"""
        SELECT * FROM users where username = "{user}" and password = "{password}"
        """
    )
    results = cursor.fetchall()
    if len(results) < 1:
        return False
    else:
        return results[0][1]


def create_users():
    global cursor
    cursor.execute(
        """
      CREATE TABLE if not exists users(
          id integer not null primary key autoincrement,
          username varchar(16) not null,
          password varchar(255) not null
      )
      """
    )


def setup():
    global conn
    global cursor
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()


def save_changes():
    global conn
    conn.commit()
    conn.close()


create_users()
