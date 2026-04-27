import psycopg2
import json
import csv
from config import load_config

def run_db_query(query, args=None, is_select=False):
    params = load_config()
    try:
        with psycopg2.connect(**params) as conn:
            conn.set_isolation_level(0)
            with conn.cursor() as cur:
                cur.execute(query, args)
                if is_select:
                    return cur.fetchall()
                if conn.notices:
                    for n in conn.notices:
                        print(f"Уведомление БД: {n.strip()}")
    except Exception as e:
        print(f"ОШИБКА: {e}")
    return None


def export_to_json():
    """3.3 Export to JSON"""
    query = "SELECT * FROM search_contacts('');" 
    rows = run_db_query(query, is_select=True)
    data = []
    for r in rows:
        data.append({
            "name": r[1], "email": r[2], 
            "birthday": str(r[3]) if r[3] else None, 
            "phones": r[4]
        })
    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("-> Данные экспортированы в contacts.json")

def import_from_json():
    """3.3 Import from JSON with Duplicate Handling"""
    try:
        with open("contacts.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for item in data:
            name = item['name']
           
            exists = run_db_query("SELECT id FROM phonebook WHERE first_name = %s", (name,), True)
            
            if exists:
                choice = input(f"Контакт '{name}' уже существует. Перезаписать? (y/n): ").lower()
                if choice != 'y':
                    continue
                
                run_db_query("DELETE FROM phonebook WHERE first_name = %s", (name,))

           
            run_db_query("INSERT INTO phonebook (first_name, email, birthday) VALUES (%s, %s, %s)", 
                        (name, item.get('email'), item.get('birthday')))
            
            
            if item.get('phones'):
                for p in item['phones'].split(', '):
                    run_db_query("CALL add_phone(%s, %s, %s)", (name, p, 'mobile'))
        print("-> Импорт завершен!")
    except FileNotFoundError:
        print("Файл contacts.json не найден. Сначала сделайте экспорт.")

def interactive_pagination():
    """3.2 Paginated navigation (Loop)"""
    limit = 5
    offset = 0
    while True:
     
        res = run_db_query("SELECT * FROM public.get_contacts_paged(%s, %s);", (limit, offset), True)
        print(f"\n--- Страница (Offset: {offset}) ---")
        if not res:
            print("Больше нет записей.")
        else:
            for r in res: print(f"ID: {r[0]} | {r[1]}: {r[2]}")
        
        cmd = input("\n[n] Next | [p] Prev | [q] Quit: ").lower()
        if cmd == 'n': offset += limit
        elif cmd == 'p': offset = max(0, offset - limit)
        elif cmd == 'q': break

def add_full_contact():
    """3.1 & 3.4 Работа с новыми полями и процедурами"""
    name = input("Имя: ")
    phone = input("Телефон: ")
    type_p = input("Тип (home, work, mobile): ")
    email = input("Email: ")
    bday = input("Birthday (YYYY-MM-DD): ") or None
    group = input("Group (Family, Work, Friend...): ")

    run_db_query("INSERT INTO phonebook (first_name, email, birthday) VALUES (%s, %s, %s)", (name, email, bday))
    run_db_query("CALL add_phone(%s, %s, %s)", (name, phone, type_p))
    run_db_query("CALL move_to_group(%s, %s)", (name, group))
    print("Готово!")


if __name__ == '__main__':
    while True:
        print("\n--- TSIS 1 MENU ---")
        print("1. Добавить контакт (Full)")
        print("2. Расширенный поиск (Имя/Email/Тел)")
        print("3. Навигация (Пагинация)")
        print("4. Экспорт в JSON")
        print("5. Импорт из JSON")
        print("0. Выход")
        
        c = input("Выбор: ")
        if c == '1': add_full_contact()
        elif c == '2':
            q = input("Запрос: ")
            res = run_db_query("SELECT * FROM search_contacts(%s)", (q,), True)
            for r in res: print(f"ID:{r[0]} | {r[1]} | Email:{r[2]} | Тел:{r[4]}")
        elif c == '3': interactive_pagination()
        elif c == '4': export_to_json()
        elif c == '5': import_from_json()
        elif c == '0': break