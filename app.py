from flask import Flask, request, jsonify, render_template
from simrs_core import generate_billing

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

if __name__ == '__main__':
    # Mode standar untuk mencegah crash (WinError 10038) di Python 3.14 Windows
    app.run(port=5000)