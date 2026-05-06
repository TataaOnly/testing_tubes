import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="simrs"
    )

def generate_billing(id_appointment):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # 1. Ambil data Appointment & Patient (TERMASUK JENIS PEMBAYARAN)
        cursor.execute("""
            SELECT a.id_patient, d.nama_dokter, p.jenis_pembayaran 
            FROM Appointments a 
            JOIN Doctors d ON a.id_doctor = d.id_doctor
            JOIN Patients p ON a.id_patient = p.id_patient
            WHERE a.id_appointment = %s
        """, (id_appointment,))
        appt = cursor.fetchone()
        
        if not appt:
            return "Appointment tidak ditemukan"

        # 2. Buat Header Invoice Baru
        cursor.execute("""
            INSERT INTO Invoices (id_patient, id_appointment, status_bayar) 
            VALUES (%s, %s, 'Belum Bayar')
        """, (appt['id_patient'], id_appointment))
        id_invoice = cursor.lastrowid

        total_biaya = 0

        # 3. Kalkulasi Kamar
        cursor.execute("SELECT tarif_per_malam, tipe_kamar FROM Rooms WHERE id_kamar = 1")
        room = cursor.fetchone()
        if room:
            subtotal_room = room['tarif_per_malam']
            cursor.execute("""
                INSERT INTO Invoice_Items (id_invoice, item_name, qty, harga_satuan, subtotal)
                VALUES (%s, %s, 1, %s, %s)
            """, (id_invoice, f"Kamar {room['tipe_kamar']}", subtotal_room, subtotal_room))
            total_biaya += subtotal_room

        # 4. Kalkulasi Obat
        cursor.execute("""
            SELECT m.nama_obat, p.jumlah, m.harga 
            FROM Prescriptions p
            JOIN Medicines m ON p.id_obat = m.id_obat
            JOIN Medical_Records mr ON p.id_record = mr.id_record
            WHERE mr.id_appointment = %s AND p.status_diambil = TRUE
        """, (id_appointment,))
        meds = cursor.fetchall()

        for med in meds:
            subtotal_med = med['jumlah'] * med['harga']
            cursor.execute("""
                INSERT INTO Invoice_Items (id_invoice, item_name, qty, harga_satuan, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_invoice, med['nama_obat'], med['jumlah'], med['harga'], subtotal_med))
            total_biaya += subtotal_med

        # --- LOGIKA BARU: VALIDASI ASURANSI / BPJS ---
        # Jika pasien menggunakan BPJS, biaya ditanggung pemerintah (total tagihan pasien jadi 0)
        if appt['jenis_pembayaran'] == 'BPJS':
            total_biaya = 0

        # 5. Update Grand Total di Invoices
        cursor.execute("UPDATE Invoices SET grand_total = %s WHERE id_invoice = %s", (total_biaya, id_invoice))
        
        conn.commit()
        return {
            "id_invoice": id_invoice, 
            "total": total_biaya, 
            "jenis_pembayaran": appt['jenis_pembayaran']
        }

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        return "Terjadi kesalahan sistem"
    finally:
        cursor.close()
        conn.close()


# ==========================================
# --- SCRIPT PENGUJIAN WHITEBOX (TEST CASES) ---
# ==========================================

# TC-01: Positive Test (Pasien Umum)
# Menguji pasien ID 1 (Pasien Umum). Total tagihan HARUS LEBIH DARI 0.
def test_generate_billing_umum():
    result = generate_billing(1)
    assert result != "Appointment tidak ditemukan"
    assert result["jenis_pembayaran"] == "Umum"
    assert result["total"] > 0

# TC-02: Edge Case Test (Pasien BPJS)
# Menguji pasien ID 2 (Pasien BPJS). Total tagihan HARUS TEPAT 0.
def test_generate_billing_bpjs():
    result = generate_billing(2)
    assert result != "Appointment tidak ditemukan"
    assert result["jenis_pembayaran"] == "BPJS"
    assert result["total"] == 0

# TC-03: Negative Test (Appointment ID tidak ada di database)
def test_generate_billing_not_found():
    result = generate_billing(999)
    assert result == "Appointment tidak ditemukan"