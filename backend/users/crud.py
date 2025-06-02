from fastapi import HTTPException,Path
from backend.db import get_connection
from backend.models import UserIn

from backend.utils.hash_password import hash_password

def create_user_db(user: UserIn):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO users (name, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            RETURNING *;
        """, (user.name, user.email, hash_password(user.password_hash), user.role))
        new_user = cur.fetchone()
        conn.commit()
        return new_user
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

def list_users_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def get_user_db(user_id: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
        user = cur.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

def delete_user_db(user_id: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        deleted_count = cur.rowcount
        conn.commit()
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": f"User {user_id} deleted successfully."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

def get_user_by_email(email: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
        user = cur.fetchone()
        return user 
    finally:
        cur.close()
        conn.close()