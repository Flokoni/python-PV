-- Задание 8.2: Процедура Upsert (Добавить или Обновить)
CREATE OR REPLACE PROCEDURE public.upsert_contact(p_name text, p_phone text)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone_number = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook (first_name, phone_number) VALUES (p_name, p_phone);
    END IF;
END;
$$;

-- Задание 8.3: Массовая вставка с валидацией номера
CREATE OR REPLACE PROCEDURE public.insert_many_contacts(p_names text[], p_phones text[])
LANGUAGE plpgsql AS $$
DECLARE i int;
BEGIN
    FOR i IN 1 .. array_upper(p_names, 1) LOOP
        -- Регулярное выражение: только цифры и длина не меньше 5
        IF p_phones[i] ~ '^[0-9]+$' AND length(p_phones[i]) >= 5 THEN
            INSERT INTO phonebook (first_name, phone_number) 
            VALUES (p_names[i], p_phones[i])
            ON CONFLICT (phone_number) DO NOTHING;
        ELSE
            -- Вывод ошибки валидации в консоль Питона
            RAISE NOTICE 'Ошибка валидации: % (%)', p_names[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$;

-- Задание 8.5: Процедура удаления по имени или телефону
CREATE OR REPLACE PROCEDURE public.delete_contact_by_data(p_target text)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook WHERE first_name = p_target OR phone_number = p_target;
END;
$$;