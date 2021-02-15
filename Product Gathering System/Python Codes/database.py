from settings import PASSWORDS
from product import Product
from user import User
from passlib.hash import pbkdf2_sha256 as hasher

import psycopg2

conn = psycopg2.connect(
            database = "postgres",
            user = "postgres",
            password = "382Emkan652",
            host = "localhost" )

class Database:
    def __init__(self, name):
        self.name = name

    def add_product(self, name, price, imported, category, info):
        cursor = conn.cursor()
        query = "INSERT INTO PRODUCTS (name, price, imported, category, info) VALUES ('{}', {}, '{}', '{}', '{}')".format(name, price, imported, category, info)
        cursor.execute(query)
        conn.commit()
        sqlite_select_query = "SELECT id from products where name = '{}'".format(name)
        cursor.execute(sqlite_select_query)
        tuple = cursor.fetchone()
        return tuple[0]

    def delete_product(self, product_key):
        cursor = conn.cursor()
        query = "DELETE FROM PRODUCTS WHERE (ID = {})".format(product_key)
        cursor.execute(query)
        conn.commit()

    def get_product(self, product_key):
        cursor = conn.cursor()
        query = "SELECT NAME, PRICE, IMPORTED, CATEGORY, INFO FROM PRODUCTS WHERE (ID = {})".format(product_key)
        cursor.execute(query)
        name, price, imported, category, info = cursor.fetchone()
        product_ = Product(name, price, imported, category, info)
        return product_
    
    def get_products(self):
        products = []
        cursor = conn.cursor()
        query = "SELECT ID, NAME, PRICE, IMPORTED, CATEGORY, INFO FROM PRODUCTS ORDER BY ID"
        cursor.execute(query)
        tuples = cursor.fetchall()
        for row in tuples:
            print(row)
            id = row[0]
            name = row[1]
            price = row[2]
            imported = row[3]
            category = row[4]
            info = row[5]
            products.append((id, Product(name,price,imported,category,info)))
        return products

    def update_product(self, product_id, name, price, imported, category, info):
        cursor = conn.cursor()
        query = "UPDATE PRODUCTS SET NAME = '{}', PRICE = {}, IMPORTED = '{}', CATEGORY = '{}', INFO = '{}' WHERE (ID = {})".format(name, price, imported, category, info, product_id)
        cursor.execute(query)
        conn.commit()

    def add_user(self, name, surname, email, password, phone_number):
        cursor = conn.cursor()
        query = "INSERT INTO USERS (name, surname, email, password, phone_number) VALUES ('{}', '{}', '{}', '{}', {})".format(name, surname, email, password, phone_number)
        cursor.execute(query)
        conn.commit()
        sqlite_select_query = "SELECT id from users where email = '{}'".format(email)
        cursor.execute(sqlite_select_query)
        tuple = cursor.fetchone()
        hashed = hasher.hash(password)
        PASSWORDS[email] = hashed
        return tuple[0]

    def delete_user(self, user_key):
        cursor = conn.cursor()
        query = "DELETE FROM USERS WHERE (ID = {})".format(user_key)
        cursor.execute(query)
        conn.commit()

    def get_user(self, user_key):
        cursor = conn.cursor()
        query = "SELECT NAME, SURNAME, EMAIL, PASSWORD, PHONE_NUMBER FROM USERS WHERE (ID = {})".format(user_key)
        cursor.execute(query)
        name, surname, email, password, phone_number = cursor.fetchone()
        user_ = User(name, surname, email, password, phone_number)
        return user_
    
    def get_users(self):
        users = []
        cursor = conn.cursor()
        query = "SELECT ID, NAME, SURNAME, EMAIL, PASSWORD, PHONE_NUMBER FROM USERS ORDER BY ID"
        cursor.execute(query)
        tuples = cursor.fetchall()
        for row in tuples:
            id = row[0]
            name = row[1]
            surname = row[2]
            email = row[3]
            password = row[4]
            phone_number = row[5]
            users.append((id, User(name, surname, email, password, phone_number)))
        return users

    def update_user(self, user_id, name, surname, email, password, phone_number):
        cursor = conn.cursor()
        query = "UPDATE USERS SET NAME = '{}', SURNAME = '{}', EMAIL = '{}', PASSWORD = '{}', PHONE_NUMBER = {} WHERE (ID = {})".format(name, surname, email, password, phone_number, user_id)
        cursor.execute(query)
        conn.commit()