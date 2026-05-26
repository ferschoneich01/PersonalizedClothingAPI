from sqlalchemy import text
from database import db

sql = """
CREATE OR REPLACE PROCEDURE sp_reset_password(
    p_email       TEXT,
    p_password    TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE users
    SET password = p_password
    WHERE email = p_email;
END;
$$;
"""

try:
    db.execute(text(sql))
    db.commit()
    print("Stored procedure created successfully.")
except Exception as e:
    db.rollback()
    print("Error:", e)
