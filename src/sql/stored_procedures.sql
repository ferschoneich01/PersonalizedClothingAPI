-- ============================================================
--  STORED PROCEDURES — PersonalizedClothingAPI (PostgreSQL)
--  Ejecutar este script una vez en tu base de datos.
-- ============================================================


-- ============================================================
--  ÓRDENES
-- ============================================================

-- 1. Obtener todas las órdenes "En proceso" (resumen por orden)
CREATE OR REPLACE FUNCTION sp_get_orders()
RETURNS TABLE (
    name          TEXT,
    lastname      TEXT,
    address       TEXT,
    city          TEXT,
    paymethod     TEXT,
    subtotal      NUMERIC,
    shippingcost  NUMERIC,
    totalAmount   NUMERIC,
    status        TEXT,
    id_status     INT,
    id_order      INT
)
LANGUAGE SQL
STABLE
AS $$
    SELECT
        p.name,
        p.lastname,
        ap.address,
        ap.city,
        pm.method,
        SUM(i.price)              AS subtotal,
        SUM(sh.cost)              AS shippingcost,
        SUM(i.price + sh.cost)    AS totalAmount,
        s.status,
        s.id_status,
        o.id_order
    FROM items i
    INNER JOIN orderdetails od  ON od.item            = i.id_item
    INNER JOIN orders o         ON o.id_order         = od.id_order
    INNER JOIN status s         ON s.id_status        = o.id_status
    INNER JOIN users u          ON u.id_user          = o.id_user
    INNER JOIN shipping sh      ON sh.id_order        = o.id_order
    INNER JOIN addres_persons ap ON ap.id_address_person = sh.address
    INNER JOIN paymentmethohds pm ON pm.id_paymentmethod = o.paymentmethod
    INNER JOIN person p         ON p.id_person        = u.person
    WHERE s.status = 'En proceso'
    GROUP BY
        o.id_order, pm.method, s.status, s.id_status,
        p.name, p.lastname, ap.address, ap.city;
$$;


-- 2. Obtener detalles de órdenes "En proceso" (por artículo)
CREATE OR REPLACE FUNCTION sp_get_order_details()
RETURNS TABLE (
    id_item      INT,
    username     TEXT,
    name         TEXT,
    color        TEXT,
    size         TEXT,
    paymethod    TEXT,
    price        NUMERIC,
    cost         NUMERIC,
    totalAmount  NUMERIC,
    status       TEXT,
    image        TEXT,
    id_status    INT,
    id_order     INT
)
LANGUAGE SQL
STABLE
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
        (i.price + sh.cost) AS totalAmount,
        s.status,
        i.image,
        s.id_status,
        o.id_order
    FROM items i
    INNER JOIN orderdetails od   ON od.item            = i.id_item
    INNER JOIN orders o          ON o.id_order         = od.id_order
    INNER JOIN status s          ON s.id_status        = o.id_status
    INNER JOIN users u           ON u.id_user          = o.id_user
    INNER JOIN shipping sh       ON sh.id_order        = o.id_order
    INNER JOIN addres_persons ap ON ap.id_address_person = sh.address
    INNER JOIN paymentmethohds p ON p.id_paymentmethod = o.paymentmethod
    WHERE s.status = 'En proceso';
$$;


-- 3. Obtener envíos (órdenes "Terminado" o "Enviado")
CREATE OR REPLACE FUNCTION sp_get_shipping()
RETURNS TABLE (
    address      TEXT,
    username     TEXT,
    name         TEXT,
    color        TEXT,
    size         TEXT,
    paymethod    TEXT,
    price        NUMERIC,
    cost         NUMERIC,
    totalAmount  NUMERIC,
    status       TEXT,
    image        TEXT,
    id_status    INT,
    id_order     INT
)
LANGUAGE SQL
STABLE
AS $$
    SELECT
        ap.address,
        u.username,
        i.name,
        od.color,
        od.size,
        p.method,
        i.price,
        sh.cost,
        (i.price + sh.cost) AS totalAmount,
        s.status,
        i.image,
        s.id_status,
        o.id_order
    FROM items i
    INNER JOIN orderdetails od   ON od.item            = i.id_item
    INNER JOIN orders o          ON o.id_order         = od.id_order
    INNER JOIN status s          ON s.id_status        = o.id_status
    INNER JOIN users u           ON u.id_user          = o.id_user
    INNER JOIN shipping sh       ON sh.id_order        = o.id_order
    INNER JOIN addres_persons ap ON ap.id_address_person = sh.address
    INNER JOIN paymentmethohds p ON p.id_paymentmethod = o.paymentmethod
    WHERE s.status IN ('Terminado', 'Enviado');
$$;


-- 4. Obtener compras de un usuario por username
CREATE OR REPLACE FUNCTION sp_get_orders_by_username(p_username TEXT)
RETURNS TABLE (
    id_item    INT,
    username   TEXT,
    name       TEXT,
    color      TEXT,
    size       TEXT,
    paymethod  TEXT,
    price      NUMERIC,
    cost       NUMERIC,
    totalAmount NUMERIC,
    status     TEXT,
    image      TEXT,
    address    TEXT,
    orderdate  TIMESTAMP
)
LANGUAGE SQL
STABLE
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
        (i.price + sh.cost) AS totalAmount,
        s.status,
        i.image,
        ap.address,
        o.orderdate
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


-- 5. Cambiar el estado de una orden
CREATE OR REPLACE PROCEDURE sp_change_order_status(
    p_id_order INT,
    p_status   TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_status INT;
BEGIN
    SELECT id_status INTO v_id_status
    FROM status
    WHERE status = p_status
    LIMIT 1;

    IF v_id_status IS NULL THEN
        RAISE EXCEPTION 'Estado no encontrado: %', p_status;
    END IF;

    UPDATE orders
    SET id_status = v_id_status
    WHERE id_order = p_id_order;
END;
$$;


-- 6. Agregar una nueva orden completa
CREATE OR REPLACE PROCEDURE sp_add_order(
    p_username TEXT,
    p_address  TEXT,
    p_color    TEXT,
    p_size     TEXT,
    p_id_item  INT,
    p_quantity INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_user    INT;
    v_id_order   INT;
    v_id_address INT;
BEGIN
    -- Obtener id_user
    SELECT id_user INTO v_id_user
    FROM users WHERE username = p_username LIMIT 1;

    IF v_id_user IS NULL THEN
        RAISE EXCEPTION 'Usuario no encontrado: %', p_username;
    END IF;

    -- Crear nueva orden
    INSERT INTO orders(orderdate, paymentmethod, id_user, id_status)
    VALUES (CURRENT_TIMESTAMP, 1, v_id_user, 1)
    RETURNING id_order INTO v_id_order;

    -- Insertar detalle de la orden
    INSERT INTO orderdetails(color, size, item, quantity, id_order)
    VALUES (p_color, p_size, p_id_item, p_quantity, v_id_order);

    -- Obtener id de dirección
    SELECT id_address_person INTO v_id_address
    FROM addres_persons
    WHERE address = p_address LIMIT 1;

    IF v_id_address IS NULL THEN
        RAISE EXCEPTION 'Dirección no encontrada: %', p_address;
    END IF;

    -- Insertar envío
    INSERT INTO shipping(shipdate, cost, id_order, address)
    VALUES (CURRENT_DATE, 70.00, v_id_order, v_id_address);
END;
$$;


-- ============================================================
--  USUARIOS
-- ============================================================

-- 7. Obtener todos los usuarios
CREATE OR REPLACE FUNCTION sp_get_users()
RETURNS TABLE (
    id_user     INT,
    username    TEXT,
    password    TEXT,
    email       TEXT,
    person      INT,
    role        INT,
    status_user INT
)
LANGUAGE SQL
STABLE
AS $$
    SELECT id_user, username, password, email, person, role, status_user
    FROM users;
$$;


-- 8. Obtener usuario por username
CREATE OR REPLACE FUNCTION sp_get_user_by_username(p_username TEXT)
RETURNS TABLE (
    id_user     INT,
    username    TEXT,
    password    TEXT,
    email       TEXT,
    person      INT,
    role        INT,
    status_user INT
)
LANGUAGE SQL
STABLE
AS $$
    SELECT id_user, username, password, email, person, role, status_user
    FROM users
    WHERE username = p_username;
$$;


-- 9. Registrar persona + usuario
CREATE OR REPLACE PROCEDURE sp_add_user(
    p_username    TEXT,
    p_password    TEXT,
    p_email       TEXT,
    p_cedula      TEXT,
    p_name        TEXT,
    p_lastname    TEXT,
    p_birthday    TEXT,
    p_phone       TEXT,
    p_city        TEXT,
    p_sex         TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_person INT;
BEGIN
    -- Insertar persona
    INSERT INTO person(cedula, name, lastname, birthday, phone, country, city, sex)
    VALUES (p_cedula, p_name, p_lastname, p_birthday::DATE, p_phone, 'Nicaragua', p_city, p_sex)
    RETURNING id_person INTO v_id_person;

    -- Insertar usuario (role=2 cliente, status_user=1 activo)
    INSERT INTO users(username, password, email, person, role, status_user)
    VALUES (p_username, p_password, p_email, v_id_person, 2, 1);
END;
$$;


-- 10. Actualizar usuario
CREATE OR REPLACE PROCEDURE sp_update_user(
    p_id_user     INT,
    p_password    TEXT,
    p_role        INT,
    p_email       TEXT,
    p_status_user INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE users
    SET password    = p_password,
        role        = p_role,
        email       = p_email,
        status_user = p_status_user
    WHERE id_user = p_id_user;
END;
$$;


-- 11. Desactivar usuario (soft delete)
CREATE OR REPLACE PROCEDURE sp_delete_user(p_id_user INT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE users SET status_user = 2 WHERE id_user = p_id_user;
END;
$$;


-- ============================================================
--  ARTÍCULOS
-- ============================================================

-- 12. Obtener todos los artículos activos
CREATE OR REPLACE FUNCTION sp_get_items()
RETURNS TABLE (
    id_item      INT,
    name         TEXT,
    description  TEXT,
    image        TEXT,
    price        NUMERIC,
    clasification INT,
    category     INT,
    status_item  INT
)
LANGUAGE SQL
STABLE
AS $$
    SELECT id_item, name, description, image, price, clasification, category, status_item
    FROM items;
$$;


-- 13. Obtener artículo por ID
CREATE OR REPLACE FUNCTION sp_get_item_by_id(p_id_item INT)
RETURNS TABLE (
    id_item       INT,
    name          TEXT,
    description   TEXT,
    image         TEXT,
    price         NUMERIC,
    clasification INT,
    category      INT,
    status_item   INT
)
LANGUAGE SQL
STABLE
AS $$
    SELECT id_item, name, description, image, price, clasification, category, status_item
    FROM items
    WHERE id_item = p_id_item;
$$;


-- 14. Obtener artículos por categoría y clasificación
CREATE OR REPLACE FUNCTION sp_get_items_by_category(p_category INT, p_clasification INT)
RETURNS TABLE (
    id_item       INT,
    name          TEXT,
    description   TEXT,
    image         TEXT,
    price         NUMERIC,
    clasification INT,
    category      INT,
    status_item   INT
)
LANGUAGE SQL
STABLE
AS $$
    SELECT id_item, name, description, image, price, clasification, category, status_item
    FROM items
    WHERE category = p_category AND clasification = p_clasification;
$$;


-- 15. Insertar artículo
CREATE OR REPLACE PROCEDURE sp_add_item(
    p_name         TEXT,
    p_description  TEXT,
    p_image        TEXT,
    p_price        NUMERIC,
    p_clasification INT,
    p_category     INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO items(name, description, image, price, clasification, category, status_item)
    VALUES (p_name, p_description, p_image, p_price, p_clasification, p_category, 1);
END;
$$;


-- 16. Actualizar artículo
CREATE OR REPLACE PROCEDURE sp_update_item(
    p_id_item      INT,
    p_name         TEXT,
    p_description  TEXT,
    p_image        TEXT,
    p_price        NUMERIC,
    p_clasification INT,
    p_category     INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE items
    SET name          = p_name,
        description   = p_description,
        image         = p_image,
        price         = p_price,
        clasification = p_clasification,
        category      = p_category
    WHERE id_item = p_id_item;
END;
$$;


-- 17. Desactivar artículo (soft delete)
CREATE OR REPLACE PROCEDURE sp_delete_item(p_id_item INT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE items SET status_item = 2 WHERE id_item = p_id_item;
END;
$$;


-- ============================================================
--  WHATSAPP / MENSAJES
-- ============================================================

-- 18. Contar mensajes por id de WhatsApp (evitar duplicados)
CREATE OR REPLACE FUNCTION sp_get_whatsapp_msg_count(p_id_wa TEXT)
RETURNS INT
LANGUAGE SQL
STABLE
AS $$
    SELECT COUNT(id)::INT FROM msgwhatsapp WHERE id_wa = p_id_wa;
$$;


-- 19. Insertar mensaje de WhatsApp
CREATE OR REPLACE PROCEDURE sp_insert_whatsapp_msg(
    p_mensaje_recibido TEXT,
    p_mensaje_enviado  TEXT,
    p_id_wa            TEXT,
    p_timestamp_wa     TEXT,
    p_telefono_wa      TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO msgwhatsapp(mensaje_recibido, mensaje_enviado, id_wa, timestamp_wa, telefono_wa)
    VALUES (p_mensaje_recibido, p_mensaje_enviado, p_id_wa, p_timestamp_wa, p_telefono_wa);
END;
$$;
