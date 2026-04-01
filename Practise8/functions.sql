-- Задание 8.1: Функция поиска по шаблону (имя или телефон)
CREATE OR REPLACE FUNCTION public.get_contacts_by_pattern(p_pattern text)
RETURNS TABLE(id int, name varchar, phone varchar) AS $$
BEGIN
    RETURN QUERY SELECT c.id, c.first_name, c.phone_number FROM phonebook c 
    WHERE c.first_name ILIKE p_pattern OR c.phone_number ILIKE p_pattern;
END;
$$ LANGUAGE plpgsql;

-- Задание 8.4: Функция для пагинации (вывод частями)
CREATE OR REPLACE FUNCTION public.get_contacts_paged(p_limit int, p_offset int)
RETURNS TABLE(id int, name varchar, phone varchar) AS $$
BEGIN
    RETURN QUERY SELECT c.id, c.first_name, c.phone_number FROM phonebook c 
    ORDER BY c.id LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;