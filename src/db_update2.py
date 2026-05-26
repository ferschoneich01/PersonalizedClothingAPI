import psycopg2
import sys

db_url = 'postgresql://postgres:rBnkurpLkOpxyFnfILEgIOFWDIaeFcyE@roundhouse.proxy.rlwy.net:11950/PCDB'

sql_commands = """
CREATE OR REPLACE PROCEDURE public.sp_create_order(IN p_username text, IN p_address text, OUT p_id_order integer)
LANGUAGE plpgsql AS $$
DECLARE
    v_id_user    INT;
    v_id_person  INT;
    v_id_address INT;
BEGIN
    SELECT id_user, person INTO v_id_user, v_id_person FROM users WHERE username = p_username LIMIT 1;
    IF v_id_user IS NULL THEN
        RAISE EXCEPTION 'Usuario no encontrado: %', p_username;
    END IF;

    -- Intentar buscar la dirección exacta para esa persona
    SELECT id_address_person INTO v_id_address 
    FROM addres_persons 
    WHERE address = p_address AND person = v_id_person 
    LIMIT 1;
    
    -- Si no existe, crearla
    IF v_id_address IS NULL THEN
        INSERT INTO addres_persons(person, address, city) 
        VALUES (v_id_person, p_address, 'Managua') 
        RETURNING id_address_person INTO v_id_address;
    END IF;

    -- Crear orden
    INSERT INTO orders(orderdate, paymentmethod, id_user, id_status)
    VALUES (CURRENT_TIMESTAMP, 1, v_id_user, 1)
    RETURNING id_order INTO p_id_order;

    -- Crear envio
    INSERT INTO shipping(shipdate, cost, id_order, address)
    VALUES (CURRENT_DATE, 70.00, p_id_order, v_id_address);
END;
$$;
"""

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute(sql_commands)
    conn.commit()
    print("Address insertion logic applied successfully.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
