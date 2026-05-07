from simrs_core import get_db_connection

def create_user(username, password, role, conn=None):
    if conn is None:
        conn = get_db_connection()
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
        conn.commit()
        return {"message": "User berhasil dibuat"}
    except Exception as e:
        return {"error": str(e)}
    
def get_user_by_username(username, conn=None):
    if conn is None:
        conn = get_db_connection()
        
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
        
    return user

def update_user_role(user_id, new_role, conn=None):
    if conn is None:
        conn = get_db_connection()
        
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = %s WHERE id_user = %s", (new_role, user_id))
        if getattr(cursor, 'rowcount', 0) == 0:
            return {"error": "User tidak ditemukan"}
        conn.commit()
        return {"message": "Role berhasil diubah"}
    except Exception as e:
        return {"error": str(e)}
