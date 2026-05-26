import psycopg2
import sys

db_url = 'postgresql://postgres:rBnkurpLkOpxyFnfILEgIOFWDIaeFcyE@roundhouse.proxy.rlwy.net:11950/PCDB'

sql_commands = """
ALTER TABLE orderdetails ADD COLUMN IF NOT EXISTS custom_image TEXT;

CREATE OR REPLACE PROCEDURE public.sp_create_order(IN p_username text, IN p_address text, OUT p_id_order integer)
LANGUAGE plpgsql AS $$
DECLARE
    v_id_user    INT;
    v_id_address INT;
BEGIN
    SELECT id_user INTO v_id_user FROM users WHERE username = p_username LIMIT 1;
    IF v_id_user IS NULL THEN
        RAISE EXCEPTION 'Usuario no encontrado: %', p_username;
    END IF;

    SELECT id_address_person INTO v_id_address FROM addres_persons WHERE address = p_address LIMIT 1;
    IF v_id_address IS NULL THEN
        RAISE EXCEPTION 'Dirección no encontrada: %', p_address;
    END IF;

    INSERT INTO orders(orderdate, paymentmethod, id_user, id_status)
    VALUES (CURRENT_TIMESTAMP, 1, v_id_user, 1)
    RETURNING id_order INTO p_id_order;

    INSERT INTO shipping(shipdate, cost, id_order, address)
    VALUES (CURRENT_DATE, 70.00, p_id_order, v_id_address);
END;
$$;

CREATE OR REPLACE PROCEDURE public.sp_add_order_detail(IN p_id_order integer, IN p_color text, IN p_size text, IN p_id_item integer, IN p_quantity integer, IN p_custom_image text)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO orderdetails(color, size, item, quantity, id_order, custom_image)
    VALUES (p_color, p_size, p_id_item, p_quantity, p_id_order, p_custom_image);
END;
$$;

DROP FUNCTION IF EXISTS public.sp_get_orders_by_username(text);
CREATE OR REPLACE FUNCTION public.sp_get_orders_by_username(p_username text)
 RETURNS TABLE(id_item integer, username text, name text, color text, size text, paymethod text, price numeric, cost numeric, totalamount numeric, status text, image text, address text, orderdate timestamp without time zone, id_order integer, quantityOrders integer, custom_image text)
 LANGUAGE sql STABLE
AS $$
    SELECT
        i.id_item,
        u.username,
        i.name,
        od.color,
        od.size,
        p.method,
        i.price,
        sh.cost,
        (i.price * od.quantity + sh.cost) AS totalAmount,
        s.status,
        COALESCE(od.custom_image, i.image) as image,
        ap.address,
        o.orderdate,
        o.id_order,
        od.quantity as quantityOrders,
        od.custom_image
    FROM items i
    INNER JOIN orderdetails od   ON od.item            = i.id_item
    INNER JOIN orders o          ON o.id_order         = od.id_order
    INNER JOIN status s          ON s.id_status        = o.id_status
    INNER JOIN users u           ON u.id_user          = o.id_user
    INNER JOIN shipping sh       ON sh.id_order        = o.id_order
    INNER JOIN addres_persons ap ON ap.id_address_person = sh.address
    INNER JOIN paymentmethohds p ON p.id_paymentmethod = o.paymentmethod
    WHERE u.username = p_username;
$$;

DROP FUNCTION IF EXISTS public.sp_get_order_details();
CREATE OR REPLACE FUNCTION public.sp_get_order_details()
 RETURNS TABLE(id_item integer, username text, name text, color text, size text, paymethod text, price numeric, cost numeric, totalamount numeric, status text, image text, id_status integer, id_order integer, quantityOrders integer, custom_image text)
 LANGUAGE sql STABLE
AS $$
    SELECT
        i.id_item,
        u.username,
        i.name,
        od.color,
        od.size,
        p.method,
        i.price,
        sh.cost,
        (i.price * od.quantity + sh.cost) AS totalAmount,
        s.status,
        COALESCE(od.custom_image, i.image) as image,
        o.id_status,
        o.id_order,
        od.quantity as quantityOrders,
        od.custom_image
    FROM items i
    INNER JOIN orderdetails od   ON od.item            = i.id_item
    INNER JOIN orders o          ON o.id_order         = od.id_order
    INNER JOIN status s          ON s.id_status        = o.id_status
    INNER JOIN users u           ON u.id_user          = o.id_user
    INNER JOIN shipping sh       ON sh.id_order        = o.id_order
    INNER JOIN paymentmethohds p ON p.id_paymentmethod = o.paymentmethod;
$$;
"""

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute(sql_commands)
    conn.commit()
    print("Database migrations applied successfully.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
