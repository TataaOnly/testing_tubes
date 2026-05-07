import json
from unittest.mock import patch

# Test for Admin User Creation
def test_create_user_success(client, db_connection):
    """Test successful user creation."""
    with patch('simrs_core.get_db_connection') as mock_db:
        # Mock the database connection and cursor
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.lastrowid = 123

        # The endpoint to test
        response = client.post('/api/users', data=json.dumps({
            'username': 'testuser',
            'password': 'password',
            'role': 'Admin'
        }), content_type='application/json')

        assert response.status_code == 201
        assert b'User berhasil dibuat' in response.data

# Test for Receptionist Patient Registration
def test_register_patient_success(client, db_connection):
    """Test successful patient registration."""
    with patch('simrs_core.get_db_connection') as mock_db:
        mock_conn = mock_db.return_value
        
        response = client.post('/api/receptionist/patients', data=json.dumps({
            'nik': '1234567890',
            'nama': 'Test Patient',
            'alamat': '123 Test St',
            'tgl_lahir': '2000-01-01'
        }), content_type='application/json')

        assert response.status_code == 201
        assert b'Pasien berhasil didaftarkan' in response.data

# Test for Doctor Medical Record Input
def test_input_medical_record_success(client, db_connection):
    """Test successful medical record input."""
    with patch('simrs_core.get_db_connection') as mock_db:
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.lastrowid = 456

        response = client.post('/api/doctor/medical_records', data=json.dumps({
            'id_patient': 1,
            'id_doctor': 1,
            'id_appointment': 1,
            'diagnosa': 'Flu',
            'tindakan': 'Istirahat'
        }), content_type='application/json')

        assert response.status_code == 201
        assert b'Rekam medis berhasil disimpan' in response.data

# Test for Pharmacist Medicine Retrieval
def test_get_medicines_success(client, db_connection):
    """Test successful retrieval of medicines."""
    with patch('simrs_core.get_db_connection') as mock_db:
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [{'id_obat': 1, 'nama_obat': 'Paracetamol', 'stok': 100, 'harga': 5000}]

        response = client.get('/api/pharmacist/medicines')

        assert response.status_code == 200
        assert b'Paracetamol' in response.data

# Test for Cashier Billing Creation
def test_create_billing_success(client, db_connection):
    """Test successful billing creation."""
    # This test will patch the generate_billing function directly
    with patch('routes.cashier_routes.generate_billing') as mock_generate_billing:
        mock_generate_billing.return_value = {'invoice_id': 789, 'total': 150000}

        response = client.post('/api/cashier/billing', data=json.dumps({
            'id_appointment': 1
        }), content_type='application/json')

        assert response.status_code == 201
        assert b'Billing berhasil dibuat' in response.data
        assert b'150000' in response.data
