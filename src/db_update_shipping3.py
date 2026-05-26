import psycopg2

db_url = 'postgresql://postgres:rBnkurpLkOpxyFnfILEgIOFWDIaeFcyE@roundhouse.proxy.rlwy.net:11950/PCDB'

sql_commands = """
DROP FUNCTION IF EXISTS public.sp_get_shipping();

CREATE OR REPLACE FUNCTION public.sp_get_shipping()
 RETURNS TABLE(
    address text, 
    username text, 
    name text, 
    color text, 
    size text, 
    paymethod text, 
    price numeric, 
    cost numeric, 
    totalamount numeric, 
    status text, 
    image text, 
    id_status integer, 
    id_order integer, 
    quantityorders integer, 
    custom_image text,
    client_name text,
    client_lastname text,
    cedula text,
    city text
 )
 LANGUAGE sql
 STABLE
AS $function$
    SELECT
        ap.address,
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
        s.id_status,
        o.id_order,
        od.quantity as quantityOrders,
        od.custom_image,
        per.name as client_name,
        per.lastname as client_lastname,
        per.cedula,
        ap.city
    FROM items i
    INNER JOIN orderdetails od   ON od.item            = i.id_item
    INNER JOIN orders o          ON o.id_order         = od.id_order
    INNER JOIN status s          ON s.id_status        = o.id_status
    INNER JOIN users u           ON u.id_user          = o.id_user
    INNER JOIN person per        ON per.id_person      = u.person
    INNER JOIN shipping sh       ON sh.id_order        = o.id_order
    INNER JOIN addres_persons ap ON ap.id_address_person = sh.address
    INNER JOIN paymentmethohds p ON p.id_paymentmethod = o.paymentmethod
    WHERE s.status IN ('Terminado', 'Enviado');
$function$;
"""

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute(sql_commands)
    conn.commit()
    print("sp_get_shipping updated successfully.")
except Exception as e:
    print(f"Error: {e}")
