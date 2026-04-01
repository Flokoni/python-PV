import psycopg2
from config import load_config

def run_db_query(query, args=None, is_select=False):
    params = load_config()
    # Печатаем, куда именно мы подключаемся для проверки
    print(f"--- Подключение к БД: {params.get('database')} ---")
    try:
        with psycopg2.connect(**params) as conn:
            conn.set_isolation_level(0) # Включаем автокоммит для процедур
            with conn.cursor() as cur:
                cur.execute(query, args)
                if is_select:
                    return cur.fetchall()
                # Печатаем сообщения от RAISE NOTICE из SQL
                if conn.notices:
                    for n in conn.notices:
                        print(f"Уведомление БД: {n.strip()}")
    except Exception as e:
        print(f"ОШИБКА В ПИТОНЕ: {e}")
    return None

if __name__ == '__main__':
    while True:
        print("\n=== ПРОВЕРКА ПРАКТИКИ 7-8 ===")
        print("1. Тест Upsert (Добавить/Обновить)")
        print("2. Тест Массовой вставки (с валидацией)")
        print("3. Тест Поиска (Pattern)")
        print("4. Тест Пагинации (Limit/Offset)")
        print("5. Тест Удаления")
        print("0. Выход")
        
        choice = input("Выбор: ")
        
        if choice == '1':
            n = input("Имя: "); p = input("Телефон: ")
            run_db_command = "CALL public.upsert_contact(%s::text, %s::text);"
            run_db_query(run_db_command, (n, p))
            print("Выполнено.")

        elif choice == '2':
            print("Запуск теста: ['Ivan', 'Sasha', 'Error'], ['87771112233', '87014445566', 'abc']")
            names = ["Ivan", "Sasha", "Error"]
            phones = ["87771112233", "87014445566", "abc"]
            run_db_query("CALL public.insert_many_contacts(%s::text[], %s::text[]);", (names, phones))
            print("Массовая вставка завершена.")

        elif choice == '3':
            pat = input("Введите часть имени или номера: ")
            res = run_db_query("SELECT * FROM public.get_contacts_by_pattern(%s::text);", (f"%{pat}%",), True)
            if res:
                for r in res: print(f"Найдено -> ID: {r[0]} | {r[1]}: {r[2]}")
            else: print("Ничего не найдено.")

        elif choice == '4':
            l = input("Сколько записей показать (Limit)?: ")
            o = input("Сколько пропустить (Offset)?: ")
            res = run_db_query("SELECT * FROM public.get_contacts_paged(%s::int, %s::int);", (l, o), True)
            if res:
                for r in res: print(f"Запись -> ID: {r[0]} | {r[1]}: {r[2]}")

        elif choice == '5':
            target = input("Имя или телефон для удаления: ")
            run_query = "CALL public.delete_contact_by_data(%s::text);"
            run_db_query(run_query, (target,))
            print(f"Запрос на удаление {target} отправлен.")

        elif choice == '0':
            break