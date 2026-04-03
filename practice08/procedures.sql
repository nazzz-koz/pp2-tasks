CREATE OR REPLACE PROCEDURE upsert_contact(p_name TEXT, p_phone TEXT)
AS $$
BEGIN
    INSERT INTO contacts(name, phone)
    VALUES (p_name, p_phone)
    ON CONFLICT (phone)
    DO UPDATE SET name = EXCLUDED.name;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE insert_many_contacts(
    names TEXT[],
    phones TEXT[]
)
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1)
    LOOP
        IF phones[i] ~ '^\+[0-9]{10,15}$' THEN
            INSERT INTO contacts(name, phone)
            VALUES (names[i], phones[i])
            ON CONFLICT (phone)
            DO UPDATE SET name = EXCLUDED.name;
        ELSE
            RAISE NOTICE 'Invalid phone: % (%)', names[i], phones[i];
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE delete_contact(p_identifier TEXT)
AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p_identifier OR phone = p_identifier;
END;
$$ LANGUAGE plpgsql;