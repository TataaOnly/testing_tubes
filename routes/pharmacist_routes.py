import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# pyrefly: ignore [missing-import]
from flask import Blueprint, jsonify, request
from simrs_core import get_db_connection

pharmacist_bp = Blueprint('pharmacist_bp', __name__)

@pharmacist_bp.route('/medicines', methods=['GET', 'POST', 'PUT'])
def manage_medicines():
    """
    UC-06: Kelola Obat
    Manages the medicine inventory.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM medicines")
        medicines = cursor.fetchall()
        return jsonify(medicines)

    if request.method == 'POST':
        data = request.get_json()
        if not all(k in data for k in ['nama_obat', 'stok', 'harga']):
            return jsonify({"error": "Data obat tidak lengkap"}), 400
        
        cursor.execute("INSERT INTO medicines (nama_obat, stok, harga) VALUES (%s, %s, %s)",
                       (data['nama_obat'], data['stok'], data['harga']))
        conn.commit()
        return jsonify({"message": "Obat berhasil ditambahkan"}), 201

    if request.method == 'PUT':
        data = request.get_json()
        if not all(k in data for k in ['id_obat', 'stok']):
            return jsonify({"error": "ID obat dan stok baru dibutuhkan"}), 400

        cursor.execute("UPDATE medicines SET stok = %s WHERE id_obat = %s",
                       (data['stok'], data['id_obat']))
        conn.commit()
        return jsonify({"message": "Stok obat berhasil diperbarui"})

    cursor.close()
    conn.close()

@pharmacist_bp.route('/prescriptions', methods=['POST'])
def process_prescription():
    """
    UC-07: Proses Resep Obat (Dispensing)
    Mengecek stok obat, mengurangi stok, dan menandai resep telah diambil.
    """
    data = request.get_json()
    id_prescription = data.get('id_prescription')
    
    if not id_prescription:
        return jsonify({"error": "id_prescription dibutuhkan"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # 1. Cek resep
        cursor.execute("SELECT * FROM prescriptions WHERE id_prescription = %s", (id_prescription,))
        prescription = cursor.fetchone()
        
        if not prescription:
            return jsonify({"error": "Resep tidak ditemukan"}), 404
            
        if prescription['status_diambil'] == 1:
            return jsonify({"error": "Obat untuk resep ini sudah diambil"}), 400
            
        id_obat = prescription['id_obat']
        jumlah = prescription['jumlah']
        
        # 2. Cek stok obat
        cursor.execute("SELECT * FROM medicines WHERE id_obat = %s", (id_obat,))
        medicine = cursor.fetchone()
        
        if not medicine:
            return jsonify({"error": "Data obat tidak ditemukan di inventaris"}), 404
            
        if medicine['stok'] < jumlah:
            return jsonify({"error": f"Stok obat tidak mencukupi (Sisa: {medicine['stok']}, Diminta: {jumlah})"}), 400
            
        # 3. Kurangi stok obat
        cursor.execute("UPDATE medicines SET stok = stok - %s WHERE id_obat = %s", (jumlah, id_obat))
        
        # 4. Tandai resep sudah diambil
        cursor.execute("UPDATE prescriptions SET status_diambil = 1 WHERE id_prescription = %s", (id_prescription,))
        
        conn.commit()
        return jsonify({
            "message": "Obat berhasil diberikan kepada pasien",
            "detail": {
                "nama_obat": medicine['nama_obat'],
                "jumlah_diberikan": jumlah
            }
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()
