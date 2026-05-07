import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="simrs"
    )

def close_db_connection(connection):
    """Fungsi untuk menutup koneksi database."""
    if connection.is_connected():
        connection.close()

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
        close_db_connection(conn)