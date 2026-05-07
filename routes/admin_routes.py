import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# pyrefly: ignore [missing-import]
from flask import Blueprint, jsonify, request
from simrs_core import get_db_connection

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/users', methods=['POST'])
def add_user():
    """
    Adds a new user to the system.
    """
    data = request.get_json()
    if not all(k in data for k in ['username', 'password', 'role']):
        return jsonify({"error": "Username, password, dan role dibutuhkan"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Note: In a real application, you MUST hash the password.
        # Storing plain text passwords is a major security risk.
        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (%s, %s, %s)
        """, (data['username'], data['password'], data['role']))
        conn.commit()
        return jsonify({"message": "User berhasil ditambahkan"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
def change_user_role(user_id):
    """
    UC-01: Mengubah Role User
    Updates the role of a specific user.
    """
    data = request.get_json()
    new_role = data.get('role')

    if not new_role:
        return jsonify({"error": "Role baru dibutuhkan"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET role = %s WHERE id_user = %s", (new_role, user_id))
        if cursor.rowcount == 0:
            return jsonify({"error": "User tidak ditemukan"}), 404
        conn.commit()
        return jsonify({"message": f"Role untuk user ID {user_id} berhasil diubah menjadi {new_role}"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
