
from flask import Flask, request, jsonify, render_template
from simrs_core import generate_billing, get_db_connection
from simrs_test.user import create_user, get_user_by_username, update_user_role
from routes.receptionist_routes import receptionist_bp
from routes.doctor_routes import doctor_bp
from routes.pharmacist_routes import pharmacist_bp
from routes.cashier_routes import cashier_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)

# --- Halaman Web Kasir ---
@app.route('/')
def home():
    return render_template('index.html')

# --- API Billing ---
@app.route('/api/billing', methods=['POST'])
def api_generate_billing():
    data = request.get_json()
    id_appointment = data.get('id_appointment')
    
    if not id_appointment:
        return jsonify({"error": "id_appointment dibutuhkan"}), 400
        
    result = generate_billing(id_appointment)
    
    if result == "Appointment tidak ditemukan":
        return jsonify({"error": result}), 404
        
    return jsonify({
        "message": "Billing berhasil dibuat",
        "data": result
    }), 201

# --- API User Creation ---
@app.route('/api/users', methods=['POST'])
def api_create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not all([username, password, role]):
        return jsonify({"error": "Username, password, dan role dibutuhkan"}), 400

    # Cek apakah peran valid
    valid_roles = ['Admin', 'Resepsionis', 'Apoteker', 'Dokter', 'Kasir']
    if role not in valid_roles:
        return jsonify({"error": f"Role tidak valid. Pilih dari: {', '.join(valid_roles)}"}), 400

    # Cek apakah username sudah ada
    if get_user_by_username(username):
        return jsonify({"error": "Username sudah digunakan"}), 409

    result = create_user(username, password, role)

    if "error" in result:
        return jsonify(result), 500

    return jsonify(result), 201

@app.route('/api/users/<int:user_id>/role', methods=['PUT'])
def api_update_user_role(user_id):
    data = request.get_json()
    new_role = data.get('role')

    if not new_role:
        return jsonify({"error": "Role baru dibutuhkan"}), 400

    valid_roles = ['Admin', 'Resepsionis', 'Apoteker', 'Dokter', 'Kasir']
    if new_role not in valid_roles:
        return jsonify({"error": f"Role tidak valid. Pilih dari: {', '.join(valid_roles)}"}), 400

    result = update_user_role(user_id, new_role)

    if "error" in result:
        if result["error"] == "User tidak ditemukan":
            return jsonify(result), 404
        return jsonify(result), 500

    return jsonify(result), 200

# Register Blueprints
app.register_blueprint(receptionist_bp, url_prefix='/api/receptionist')
app.register_blueprint(doctor_bp, url_prefix='/api/doctor')
app.register_blueprint(pharmacist_bp, url_prefix='/api/pharmacist')
app.register_blueprint(cashier_bp, url_prefix='/api/cashier')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

if __name__ == '__main__':
    # Mode standar untuk mencegah crash (WinError 10038) di Python 3.14 Windows
    app.run(port=5000)

# --- Tests from simrs_core.py, adapted for pytest ---

def test_generate_billing_umum():
    """TC-01: Positive Test (Pasien Umum)"""
    # Menguji pasien ID 1 (Pasien Umum). Total tagihan HARUS LEBIH DARI 0.
    result = generate_billing(1)
    assert result != "Appointment tidak ditemukan"
    assert result["jenis_pembayaran"] == "Umum"
    assert result["total"] > 0

def test_generate_billing_bpjs():
    """TC-02: Edge Case Test (Pasien BPJS)"""
    # Menguji pasien ID 2 (Pasien BPJS). Total tagihan HARUS TEPAT 0.
    result = generate_billing(2)
    assert result != "Appointment tidak ditemukan"
    assert result["jenis_pembayaran"] == "BPJS"
    assert result["total"] == 0

def test_generate_billing_not_found():
    """TC-03: Negative Test (Appointment ID tidak ada di database)"""
    result = generate_billing(999)
    assert result == "Appointment tidak ditemukan"

def test_get_medicine(db_connection):
    """Test retrieving an existing medicine's data."""
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medicines WHERE id_obat = 1")
    medicine = cursor.fetchone()
    assert medicine is not None
    assert medicine['nama_obat'] == 'Amoxicillin'

def test_create_medical_record(db_connection):
    """Test creating a new medical record."""
    cursor = db_connection.cursor()
    
    # Assuming patient 1, doctor 1, and appointment 1 exist
    cursor.execute("""
        INSERT INTO medical_records (id_patient, id_doctor, id_appointment, diagnosa, tindakan) 
        VALUES (1, 1, 1, 'Test Diagnose', 'Test Action')
    """)
    record_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM medical_records WHERE id_record = %s", (record_id,))
    record = cursor.fetchone()
    
    assert record is not None
    
    # Clean up
    cursor.execute("DELETE FROM medical_records WHERE id_record = %s", (record_id,))

def test_get_room(db_connection):
    """Test retrieving an existing room's data."""
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rooms WHERE id_kamar = 1")
    room = cursor.fetchone()
    assert room is not None
    assert room['tipe_kamar'] == 'VIP'

def test_get_user(db_connection):
    """Test retrieving an existing user's data."""
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id_user = 1")
    user = cursor.fetchone()
    assert user is not None
    assert user['username'] == 'admin_simrs'