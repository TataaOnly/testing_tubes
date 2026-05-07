import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# pyrefly: ignore [missing-import]
from flask import Blueprint, jsonify, request
from simrs_core import get_db_connection

receptionist_bp = Blueprint('receptionist_bp', __name__)

@receptionist_bp.route('/patients', methods=['POST'])
def register_patient():
    """
    UC-02: Mendaftarkan Pasien
    Registers a new patient in the system.
    """
    data = request.get_json()
    # Basic validation
    if not all(k in data for k in ['nik', 'nama', 'alamat', 'tgl_lahir']):
        return jsonify({"error": "Data pasien tidak lengkap"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO patients (nik, nama, alamat, tgl_lahir, jenis_pembayaran, nomor_asuransi)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['nik'], data['nama'], data['alamat'], data['tgl_lahir'],
            data.get('jenis_pembayaran', 'Umum'), data.get('nomor_asuransi')
        ))
        conn.commit()
        return jsonify({"message": "Pasien berhasil didaftarkan"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@receptionist_bp.route('/appointments', methods=['POST'])
def schedule_doctor():
    """
    UC-03: Menjadwalkan Dokter
    Schedules a new appointment for a patient with a doctor.
    """
    data = request.get_json()
    if not all(k in data for k in ['id_patient', 'id_doctor', 'jadwal']):
        return jsonify({"error": "Data appointment tidak lengkap"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO appointments (id_patient, id_doctor, jadwal)
            VALUES (%s, %s, %s)
        """, (data['id_patient'], data['id_doctor'], data['jadwal']))
        conn.commit()
        return jsonify({"message": "Jadwal dokter berhasil dibuat"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@receptionist_bp.route('/rooms', methods=['GET'])
def manage_rooms():
    """
    UC-04: Manajemen Kamar
    Gets the status of all rooms.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_kamar, tipe_kamar, status_tersedia, tarif_per_malam FROM rooms")
        rooms = cursor.fetchall()
        return jsonify(rooms)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
