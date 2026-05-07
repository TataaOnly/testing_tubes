import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Blueprint, jsonify, request
from simrs_core import get_db_connection

doctor_bp = Blueprint('doctor_bp', __name__)

@doctor_bp.route('/medical_records', methods=['POST'])
def input_medical_record():
    """
    UC-05: Input Rekam Medis
    Creates a new medical record for a patient.
    """
    data = request.get_json()
    if not all(k in data for k in ['id_patient', 'id_doctor', 'id_appointment', 'diagnosa', 'tindakan']):
        return jsonify({"error": "Data rekam medis tidak lengkap"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO medical_records (id_patient, id_doctor, id_appointment, diagnosa, tindakan)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['id_patient'], data['id_doctor'], data['id_appointment'], data['diagnosa'], data['tindakan']))
        conn.commit()
        return jsonify({"message": "Rekam medis berhasil ditambahkan"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@doctor_bp.route('/prescriptions', methods=['POST'])
def create_prescription():
    """
    UC-05: Pembuatan Resep Obat
    Creates a new prescription for a patient.
    """
    data = request.get_json()
    if not all(k in data for k in ['id_record', 'id_obat', 'jumlah']):
        return jsonify({"error": "Data resep tidak lengkap"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO prescriptions (id_record, id_obat, jumlah)
            VALUES (%s, %s, %s)
        """, (data['id_record'], data['id_obat'], data['jumlah']))
        conn.commit()
        return jsonify({"message": "Resep berhasil dibuat"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
