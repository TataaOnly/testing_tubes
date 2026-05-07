import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Blueprint, jsonify, request
from simrs_core import generate_billing, get_db_connection

cashier_bp = Blueprint('cashier_bp', __name__)

@cashier_bp.route('/billing', methods=['POST'])
def process_billing():
    """
    UC-08: Pembuatan Billing
    Generates a new bill for an appointment.
    """
    data = request.get_json()
    id_appointment = data.get('id_appointment')
    
    if not id_appointment:
        return jsonify({"error": "id_appointment dibutuhkan"}), 400
        
    result = generate_billing(id_appointment)
    
    if isinstance(result, str):
        return jsonify({"error": result}), 404
        
    return jsonify({
        "message": "Billing berhasil dibuat",
        "data": result
    }), 201

@cashier_bp.route('/invoices/<int:invoice_id>/status', methods=['PUT'])
def update_payment_status(invoice_id):
    """
    UC-08: Ubah Status Bayar
    Updates the payment status of an invoice.
    """
    data = request.get_json()
    new_status = data.get('status_bayar')

    if not new_status:
        return jsonify({"error": "Status bayar baru dibutuhkan"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE invoices SET status_bayar = %s WHERE id_invoice = %s", (new_status, invoice_id))
        if cursor.rowcount == 0:
            return jsonify({"error": "Invoice tidak ditemukan"}), 404
        conn.commit()
        return jsonify({"message": f"Status bayar untuk invoice ID {invoice_id} berhasil diubah menjadi {new_status}"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@cashier_bp.route('/invoices', methods=['GET'])
def search_invoices():
    """
    UC-08: Cari Invoice by Nama Pasien
    Searches for invoices based on a patient's name.
    """
    patient_name = request.args.get('patient_name')

    if not patient_name:
        return jsonify({"error": "Nama pasien dibutuhkan"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # This query joins invoices with appointments and patients to filter by patient name
        query = """
            SELECT i.*, p.nama 
            FROM invoices i
            JOIN appointments a ON i.id_appointment = a.id_appointment
            JOIN patients p ON a.id_patient = p.id_patient
            WHERE p.nama LIKE %s
        """
        cursor.execute(query, (f"%{patient_name}%",))
        invoices = cursor.fetchall()
        
        if not invoices:
            return jsonify({"message": "Tidak ada invoice yang ditemukan untuk pasien ini"}), 404
            
        return jsonify(invoices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
