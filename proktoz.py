import sqlite3

class Database:
    conn = sqlite3.connect('pizzeria.db')
    cursor = conn.cursor()

    @classmethod
    def create_tables(cls):
        cls.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT NOT NULL
            )
        ''')
        cls.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                products TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        cls.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tovars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        cls.conn.commit()

    @classmethod
    def add_user(cls, user):
        cls.cursor.execute('''
            INSERT INTO users (username, password, role, full_name)
            VALUES (?, ?, ?, ?)
        ''', (user.username, user.password, user.role, user.full_name))
        cls.conn.commit()

    @classmethod
    def add_order(cls, order):
        cls.cursor.execute('''
            INSERT INTO orders (user_id, products)
            VALUES (?, ?)
        ''', (order.user.id, order.products))
        cls.conn.commit()

    @classmethod
    def add_tovar(cls, tovar):
        cls.cursor.execute('''
            INSERT INTO tovars (name, price, quantity)
            VALUES (?, ?, ?)
        ''', (tovar.name, tovar.price, tovar.quantity))
        cls.conn.commit()

    @classmethod
    def fetch_user(cls, username, password):
        cls.cursor.execute('''
            SELECT * FROM users
            WHERE username = ? AND password = ?
        ''', (username, password))
        user_data = cls.cursor.fetchone()

        if user_data:
            user_id, username, password, role, full_name = user_data
            return User(user_id, username, password, role, full_name)
        else:
            return None

    @classmethod
    def delete_order(cls, order_id):
        cls.cursor.execute('''
            DELETE FROM orders
            WHERE id = ?
        ''', (order_id,))
        cls.conn.commit()

class User:
    def __init__(self, user_id, username, password, role, full_name):
        self.id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.full_name = full_name

class Order:
    def __init__(self, order_id, user, products):
        self.id = order_id
        self.user = user
        self.products = products

class Tovar:
    def __init__(self, tovar_id, name, price, quantity):
        self.id = tovar_id
        self.name = name
        self.price = price
        self.quantity = quantity

class Interface:
    @staticmethod
    def register():
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        role = input("Выберите роль (Клиент/Сотрудник): ")
        full_name = input("Введите ваше полное имя: ")

        user = User(None, username, password, role, full_name)
        Database.add_user(user)
        print("Регистрация прошла успешно!")

    @staticmethod
    def login():
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        user = Database.fetch_user(username, password)

        if user:
            return user
        else:
            print("Неверное имя пользователя или пароль.")
            return None



    @classmethod
    def main(cls):
        pass

    @staticmethod
    def view_products():

        Database.cursor.execute("SELECT * FROM tovars")
        products = Database.cursor.fetchall()


        if products:
            print("Список товаров:")
            for product in products:
                tovar_id, name, price, quantity = product
                print(f"ID: {tovar_id}, Название: {name}, Цена: {price}, Количество: {quantity}")
        else:
            print("В базе данных нет товаров.")

    @staticmethod
    def add_to_cart():
        tovar_id = input("Введите ID товара, который хотите добавить в корзину: ")
        quantity = int(input("Введите количество товара: "))


        Database.cursor.execute("SELECT * FROM tovars WHERE id = ?", (tovar_id,))
        product = Database.cursor.fetchone()

        if product:

            user_id = 1
            order = Order(None, User(user_id, None, None, None, None), f"{tovar_id}:{quantity}")


            Database.add_order(order)
            print("Товар успешно добавлен в корзину!")
        else:
            print("Товар с указанным ID не найден.")

    @classmethod
    def change_order(cls, order_id, new_products):
        cls.cursor.execute('''
                UPDATE orders
                SET products = ?
                WHERE id = ?
            ''', (new_products, order_id))
        cls.conn.commit()

    @classmethod
    def delete_product(product_id):
        Database.cursor.execute('''
                      DELETE FROM products
                      WHERE id = ?
                  ''', (product_id,))
        Database.conn.commit()



    @staticmethod
    def change_order():
        order_id = input("Введите ID заказа, который хотите изменить: ")
        new_products = input("Введите новый список товаров: ")

        Database.cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order = Database.cursor.fetchone()

        if order:
            Database.change_order(order_id, new_products)
            print("Заказ успешно изменен!")
        else:
            print("Заказ с указанным ID не найден.")

    @classmethod
    def delete_order(cls):
        order_id = input("Введите ID заказа, который хотите удалить: ")

        Database.cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order = Database.cursor.fetchone()

        if order:
            cls.delete_order_by_id(order_id)
            print("Заказ успешно удален!")
        else:
            print("Заказ с указанным ID не найден.")

    @staticmethod
    def delete_order(order_id):
        Database.delete_order(order_id)
        print("Заказ успешно удален!")

    @staticmethod
    def client_interface():
        print("Добро пожаловать в интерфейс клиента!")
        while True:
            choice = input(
                "1. Просмотр товаров\n2. Добавить товар в корзину\n3. Изменить заказ\n4. Удалить заказ\n5. Выйти\nВыберите действие: ")
            if choice == "1":
                Interface.view_products()
            elif choice == "2":
                Interface.add_to_cart()
            elif choice == "3":
                Interface.change_order()
            elif choice == "4":
                order_id = input("Введите ID заказа, который хотите удалить: ")
                Interface.delete_order(order_id)
                pass
            elif choice == "5":
                return
            else:
                print("Неверный ввод. Пожалуйста, выберите корректное действие.")

    @staticmethod
    def add_tovar():
        name = input("Введите название товара: ")
        price = float(input("Введите цену товара: "))
        quantity = int(input("Введите количество товара: "))

        tovar = Tovar(None, name, price, quantity)
        Database.add_tovar(tovar)
        print("Товар успешно добавлен!")

    @staticmethod
    def delete_tovar():
        tovar_id = input("Введите ID товара, который хотите удалить: ")
        Database.cursor.execute("SELECT * FROM tovars WHERE id = ?", (tovar_id,))
        tovar = Database.cursor.fetchone()

        if tovar:
            Database.cursor.execute("DELETE FROM tovars WHERE id = ?", (tovar_id,))
            Database.conn.commit()
            print("Товар успешно удален!")
        else:
            print("Товар с указанным ID не найден.")



    @staticmethod
    def update_tovar():
        tovar_id = input("Введите ID товара, который хотите изменить: ")

        Database.cursor.execute("SELECT * FROM tovars WHERE id = ?", (tovar_id,))
        product = Database.cursor.fetchone()

        if product:
            tovar_id, name, price, quantity = product
            print(f"Текущие данные товара (ID: {tovar_id}):")
            print(f"Название: {name}, Цена: {price}, Количество: {quantity}")

            new_name = input("Введите новое название товара (или Enter, чтобы оставить без изменений): ")
            new_price = float(input("Введите новую цену товара (или Enter, чтобы оставить без изменений): "))
            new_quantity = int(input("Введите новое количество товара (или Enter, чтобы оставить без изменений): "))

            if new_name:
                product = (new_name, new_price, new_quantity, tovar_id)
                Database.cursor.execute('''
                    UPDATE tovars
                    SET name = ?, price = ?, quantity = ?
                    WHERE id = ?
                ''', product)
                Database.conn.commit()

            print("Товар успешно изменен!")
        else:
            print("Товар с указанным ID не найден.")

    @staticmethod
    def update_user():
        username = input("Введите имя пользователя, данные которого хотите изменить: ")

        Database.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = Database.cursor.fetchone()

        if user_data:
            user_id, current_username, password, role, full_name = user_data
            print(f"Текущие данные пользователя (ID: {user_id}):")
            print(f"Имя пользователя: {current_username}, Роль: {role}, Полное имя: {full_name}")

            new_username = input("Введите новое имя пользователя (или Enter, чтобы оставить без изменений): ")
            new_role = input("Введите новую роль пользователя (или Enter, чтобы оставить без изменений): ")
            new_full_name = input("Введите новое полное имя пользователя (или Enter, чтобы оставить без изменений): ")

            if new_username:
                user = (new_username, new_role, new_full_name, username)
                Database.cursor.execute('''
                    UPDATE users
                    SET username = ?, role = ?, full_name = ?
                    WHERE username = ?
                ''', user)
                Database.conn.commit()

            print("Данные пользователя успешно изменены!")
        else:
            print("Пользователь с указанным именем не найден.")


    @staticmethod
    def employee_interface():
        print("Добро пожаловать в интерфейс сотрудника!")
        while True:
            choice = input(
                "1. Добавить товар\n2. Удалить товар\n3. Изменить товар\n4. Изменить данные клиента\n5. Выйти\nВыберите действие: "
            )
            if choice == "1":
                Interface.add_tovar()
            elif choice == "2":
                Interface.delete_tovar()
            elif choice == "3":
                Interface.update_tovar()
            elif choice == "4":
                Interface.update_user()
            elif choice == "5":
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите корректное действие.")

    @staticmethod
    def main():
        while True:
            choice = input("1. Регистрация\n2. Авторизация\n3. Выход\nВыберите действие: ")

            if choice == "1":
                Interface.register()
            elif choice == "2":
                user = Interface.login()
                if user and user.role == "Клиент":
                    Interface.client_interface()
                elif user and user.role == "Сотрудник":
                    Interface.employee_interface()
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите корректное действие.")


    peperoni = Tovar(None, "Peperoni", 599, 99)
    margarita = Tovar(None, "Margarite", 999, 100)
    paramech = Tovar(None, "paramech", 5599999999, 1)

    Database.add_tovar(peperoni)
    Database.add_tovar(margarita)
    Database.add_tovar(paramech)

    

if __name__ == "__main__":
    Database.create_tables()
    Interface.main()
