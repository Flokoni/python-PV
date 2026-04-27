
CREATE OR REPLACE PROCEDURE add_phone(p_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id INTO v_id FROM phonebook WHERE first_name = p_name;
    IF v_id IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_id, p_phone, p_type);
    ELSE
        RAISE NOTICE 'Контакт % не найден', p_name;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(p_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INTEGER;
BEGIN

    INSERT INTO groups (name) VALUES (p_group_name)
    ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
    RETURNING id INTO v_group_id;

    UPDATE phonebook SET group_id = v_group_id WHERE first_name = p_name;
END;
$$;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INTEGER, name VARCHAR, email VARCHAR, birthday DATE, phones TEXT) 
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY 
    SELECT c.id, c.first_name, c.email, c.birthday, string_agg(p.phone, ', ')
    FROM phonebook c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%' 
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id;
END;
$$;