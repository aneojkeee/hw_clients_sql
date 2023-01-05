import psycopg2
from pprint import pprint

# def delete_db(cur):
#     cur.execute("""
#         DROP TABLE client_phonenums;
#         DROP TABLE clients;
#         """)

def create_db(cur):
    # Таблицы основных данных о клиенте
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY, 
        first_name VARCHAR(100) NOT NULL, 
        last_name VARCHAR(100) NOT NULL, 
        client_email VARCHAR(100) NOT NULL);
        """)

    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS client_phonenums(
        id_phonenum SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL REFERENCES clients(id),
        client_phonenum VARCHAR(40) UNIQUE);
        """)

def add_client(cur, first_name, last_name, client_email):
    cur.execute("""
        INSERT INTO clients (first_name, last_name, client_email)
        VALUES (%s, %s, %s)
        """, (first_name, last_name, client_email))
    return

def add_phone(cur, client_id, phonenumber):
    cur.execute("""
        INSERT INTO client_phonenums(client_id, client_phonenum) 
        VALUES(%s, %s)
        """, (client_id, phonenumber))
    return

def change_client_data():
    # Изменение данных о клиенте
    print("Выберите нужную команду для изменения даннных: \n "
        "1 - изменить имя клиента; 2 - изменить фамилию клиента; 3 - изменить email; 4 - изменить номер телефона")

    while True:
        input_symbol = int(input())
        if input_symbol == 1:
            input_id_change_name = input("Введите id клиента необходимого для изменений: ")
            input_name_change = input("Введите имя для замены: ")
            cur.execute("""
                UPDATE clients 
                SET first_name=%s 
                WHERE id=%s;
                """, (input_name_change, input_id_change_name))
            break

        elif input_symbol == 2:
            input_id_change_surname = input("Введите id клиента необходимого для изменений: ")
            input_surname_change = input("Введите фамилию для замены: ")
            cur.execute("""
                UPDATE clients 
                SET last_name=%s 
                WHERE id=%s;
                """, (input_surname_change, input_id_change_surname))
            break

        elif input_symbol == 3:
            input_id_change_email = input("Введите id клиента необходимого для изменений: ")
            input_email_change = input("Введите e-mail для замены: ")
            cur.execute("""
                UPDATE clients 
                SET client_email=%s 
                WHERE id=%s;
                """, (input_email_change, input_id_change_email))
            break

        elif input_symbol == 4:
            input_phonenum_change = input("Введите номер телефона который необходимо изменить: ")
            input_phonenum_for_changing = input("Введите новый номер телефона для замены: ")
            cur.execute("""
                UPDATE client_phonenums 
                SET client_phonenum=%s 
                WHERE client_phonenum=%s;
                """, (input_phonenum_for_changing, input_phonenum_change))
            break

        else:
            print("Введена неправильная команда, повторите ввод: ")

def delete_phone():
    # Удаление номера телефона из таблицы - "client_phonenums"
    input_id_del_phonenums = input("Введите id клиента номер телефона которого необходимо удалить: ")
    input_phonenum_deleting = input("Введите номер телефона который хотите удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client_phonenums 
            WHERE client_id=%s AND client_phonenum=%s
            """, (input_id_del_phonenums, input_phonenum_deleting))

def delete_client():
    # Удаление информации о клиенте
    input_id_client_del = input("Введите id клиента которого необходимо удалить: ")
    input_lastname_del = input("Введите фамилию клиента которого необходимо удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client_phonenums 
            WHERE client_id=%s
            """, (input_id_client_del))

        cur.execute("""
            DELETE FROM clients    
            WHERE id=%s AND last_name=%s
            """, (input_id_client_del, input_lastname_del))

def find_client():
    # Поиск клиента по имени
    print("Для поиска информации о клиенте, введите команду:\n "
          "1 - по имени; 2 - по фамилии; 3 - по e-mail; 4 - по номеру телефона")
    while True:
        input_finding = int(input("Введите команду для поиска информации о клиенте: "))
        if input_finding == 1:
            input_name_finding = input("Введите имя для поиска информации о клиенте: ")
            cur.execute("""
                SELECT id, first_name, last_name, client_email, client_phonenum FROM clients c
                LEFT JOIN client_phonenums cp ON cp.id_phonenum = c.id
                WHERE first_name=%s
                """, (input_name_finding,))
            print(cur.fetchall())

        elif input_finding == 2:
            input_surname_finding = input("Введите фамилию для поиска информации о клиенте: ")
            cur.execute("""
                SELECT id, first_name, last_name, client_email, client_phonenum FROM clients c
                LEFT JOIN client_phonenums cp ON cp.id_phonenum = c.id
                WHERE last_name=%s
                """, (input_surname_finding,))
            print(cur.fetchall())

        elif input_finding == 3:
            input_email_finding = input("Введите email для поиска информации о клиенте: ")
            cur.execute("""
                SELECT id, first_name, last_name, client_email, client_phonenum FROM clients c
                LEFT JOIN client_phonenums cp ON cp.id_phonenum = c.id
                WHERE client_email=%s
                """, (input_email_finding,))
            print(cur.fetchall())

        elif input_finding == 4:
            input_phonenumber_finding = input("Введите номер телефона для поиска информации о клиенте: ")
            cur.execute("""
                SELECT id, first_name, last_name, client_email, client_phonenum FROM clients c
                LEFT JOIN client_phonenums cp ON cp.id_phonenum = c.id
                WHERE client_phonenum=%s
                """, (input_phonenumber_finding,))
            print(cur.fetchall())

        else:
            print("Введена неправильная команда, повторите ввод: ")

def check_function(cur):
    # Проверочная функция, отображает содержимое таблиц
    cur.execute("""
        SELECT * FROM clients;
        """)
    pprint(cur.fetchall())
    cur.execute("""
        SELECT * FROM client_phonenums;
        """)
    pprint(cur.fetchall())

with psycopg2.connect(database="clients_db", user="postgres", password="6522") as conn:
    with conn.cursor() as cur:
        create_db(cur)
        check_function(cur)
        add_client(cur, "Леонид", "Петров", "leopetrov@gmail.com")
        add_client(cur, "Евгений", "Третьяков", "evtretyak@gmail.com")
        add_client(cur, "Максим", "Полунин", "maxpolunin@inbox.ru")
        add_client(cur, "Артем", "Ахматов", "artakhmat@yandex.ru")
        add_client(cur, "Маркус", "Эрнендес", "markushern@gmail.com")
        add_phone(cur, 1, "88008888888")
        add_phone(cur, 2, "89009999999")
        add_phone(cur, 3, "87007777777")
        add_phone(cur, 4, "86016661111")
        add_phone(cur, 5, "89209999922")
        change_client_data()
        delete_phone()
        delete_client()
        find_client()
conn.close()