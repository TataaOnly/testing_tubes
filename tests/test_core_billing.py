import pytest
from simrs_core import generate_billing

def test_generate_billing_umum(db_connection):
    """TC-01: Positive Test (Pasien Umum)"""
    # This test requires appointment ID 1 to exist and be for a 'Umum' patient.
    # Setup: Ensure appointment 1 exists with patient type 'Umum' and has associated items.
    cursor = db_connection.cursor()
    # Clean up previous invoice if it exists to ensure a clean run
    cursor.execute("DELETE FROM invoice_items WHERE id_invoice IN (SELECT id_invoice FROM invoices WHERE id_appointment = 1)")
    cursor.execute("DELETE FROM invoices WHERE id_appointment = 1")
    db_connection.commit()

    result = generate_billing(1)
    assert result is not None
    assert "error" not in result
    assert result["jenis_pembayaran"] == "Umum"
    assert result["total"] > 0

def test_generate_billing_bpjs(db_connection):
    """TC-02: Edge Case Test (Pasien BPJS)"""
    # This test requires appointment ID 2 to exist and be for a 'BPJS' patient.
    # Setup: Ensure appointment 2 exists with patient type 'BPJS'.
    cursor = db_connection.cursor()
    # Clean up previous invoice if it exists to ensure a clean run
    cursor.execute("DELETE FROM invoice_items WHERE id_invoice IN (SELECT id_invoice FROM invoices WHERE id_appointment = 2)")
    cursor.execute("DELETE FROM invoices WHERE id_appointment = 2")
    db_connection.commit()

    result = generate_billing(2)
    assert result is not None
    assert "error" not in result
    assert result["jenis_pembayaran"] == "BPJS"
    assert result["total"] == 0

def test_generate_billing_not_found():
    """TC-03: Negative Test (Appointment ID tidak ada di database)"""
    result = generate_billing(999)
    assert result == "Appointment tidak ditemukan"
