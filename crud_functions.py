import sqlite3


def initiate_db():

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    ''')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER TEXT NOT NULL)''')


    conn.commit()
    conn.close()

def add_user(username, email, age):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)", (username, email, age, 1000))
    conn.commit()
    conn.close()

def is_included(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    check_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
    if check_user is None:
        return False
    conn.commit()
    return True

def add_product(title, description, price):

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', (title, description, price))
    conn.commit()
    conn.close()


def get_all_products():

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    conn.close()
    return products


if __name__ == "__main__":
    initiate_db()
    add_product("Product1", "APPLE", 100)
    add_product("Product2", "lemon", 200)
    add_product("Product3", "orange", 300)
    add_product("Product4", "pear", 400)

    add_user("newuser", "user@gmail.com", 33)
    add_user("seconduser", "ex1@gmail.com", 22)

    us1 = is_included("newuser")
    print(us1)
    us2 = is_included("newuser1")
    print(us2)

