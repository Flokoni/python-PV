import psycopg2
import csv
from config import load_config

# 1 (Design table)
def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        phone_number VARCHAR(20) NOT NULL UNIQUE
    )
    """
    params = load_config()
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            print("Таблица 'phonebook' готова к работе.")

# 2 (Insert from CSV)
def insert_from_csv(file_path):
    params = load_config()
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        
                        cur.execute(
                            "INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s) ON CONFLICT (phone_number) DO NOTHING",
                            row
                        )
                print(f"Данные из {file_path} успешно загружены.")
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")

# 3 (Insert from console)
def add_contact_manual():
    name = input("Введите имя: ")
    phone = input("Введите номер телефона: ")
    params = load_config()
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)", (name, phone))
            print("Контакт успешно добавлен вручную.")

# 4(Update contact)
def update_contact(old_name, new_phone):
    params = load_config()
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE phonebook SET phone_number = %s WHERE first_name = %s", (new_phone, old_name))
            print(f"Контакт {old_name} обновлен.")

# 5 (Querying with filters)
def search_contacts(pattern):
    params = load_config()
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
        
            cur.execute("SELECT * FROM phonebook WHERE first_name LIKE %s OR phone_number LIKE %s", 
                        (f'%{pattern}%', f'{pattern}%'))
            rows = cur.fetchall()
            print("\n--- Результаты поиска ---")
            for row in rows:
                print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")

# 6 (Deleting)
def delete_contact(name_or_phone):
    params = load_config()
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE first_name = %s OR phone_number = %s", 
                        (name_or_phone, name_or_phone))
            print(f"Запись '{name_or_phone}' удалена.")


if __name__ == '__main__':
    create_table()
    
    while True:
        print("\n1. Загрузить из CSV\n2. Добавить вручную\n3. Обновить контакт\n4. Поиск\n5. Удалить\n0. Выход")
        choice = input("Выберите действие: ")
        
        if choice == '1':
            insert_from_csv('contacts.csv')
        elif choice == '2':
            add_contact_manual()
        elif choice == '3':
            name = input("Введите имя контакта для изменения: ")
            new_p = input("Введите новый телефон: ")
            update_contact(name, new_p)
        elif choice == '4':
            pat = input("Введите имя или префикс номера для поиска: ")
            search_contacts(pat)
        elif choice == '5':
            target = input("Введите имя или номер для удаления: ")
            delete_contact(target)
        elif choice == '0':
            break

# 7 (Show all)
def show_all_contacts():
    """ Показывает всё содержимое таблицы """
    params = load_config()
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM phonebook ORDER BY id;")
                rows = cur.fetchall()
                print("\n=== СОДЕРЖИМОЕ БАЗЫ ДАННЫХ ===")
                for row in rows:
                    print(f"ID: {row[0]} | Имя: {row[1]} | Номер: {row[2]}")
                if not rows:
                    print("Таблица пуста.")
                print("==============================")
    except Exception as e:
        print(f"Ошибка при выводе данных: {e}")