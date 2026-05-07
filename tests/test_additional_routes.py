# pyrefly: ignore [missing-import]
import pytest
from unittest.mock import patch
# pyrefly: ignore [missing-import]
from flask import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_admin_add_user(client):
    with patch('routes.admin_routes.get_db_connection') as mock_db:
        mock_conn = mock_db.return_value
        response = client.post('/api/admin/users', data=json.dumps({
            'username': 'admin_new', 'password': '123', 'role': 'Admin'
        }), content_type='application/json')
        assert response.status_code == 201

def test_admin_change_role(client):
    with patch('routes.admin_routes.get_db_connection') as mock_db:
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.rowcount = 1
        response = client.put('/api/admin/users/1/role', data=json.dumps({
            'role': 'Kasir'
        }), content_type='application/json')
        assert response.status_code == 200

def test_receptionist_manage_rooms(client):
    with patch('routes.receptionist_routes.get_db_connection') as mock_db:
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [{'id_kamar': 1, 'tipe_kamar': 'VIP'}]
        response = client.get('/api/receptionist/rooms')
        assert response.status_code == 200

def test_receptionist_schedule_doctor(client):
    with patch('routes.receptionist_routes.get_db_connection') as mock_db:
        mock_conn = mock_db.return_value
        response = client.post('/api/receptionist/appointments', data=json.dumps({
            'id_patient': 1, 'id_doctor': 1, 'jadwal': '2024-01-01'
        }), content_type='application/json')
        assert response.status_code == 201

def test_doctor_create_prescription(client):
    with patch('routes.doctor_routes.get_db_connection') as mock_db:
        mock_conn = mock_db.return_value
        response = client.post('/api/doctor/prescriptions', data=json.dumps({
            'id_record': 1, 'id_obat': 1, 'jumlah': 2
        }), content_type='application/json')
        assert response.status_code == 201

def test_pharmacist_manage_medicines_get(client):
    with patch('routes.pharmacist_routes.get_db_connection') as mock_db:
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [{'id_obat': 1, 'nama_obat': 'Panadol'}]
        response = client.get('/api/pharmacist/medicines')
        assert response.status_code == 200

def test_pharmacist_manage_medicines_post(client):
    with patch('routes.pharmacist_routes.get_db_connection') as mock_db:
        mock_conn = mock_db.return_value
        response = client.post('/api/pharmacist/medicines', data=json.dumps({
            'nama_obat': 'Obat', 'stok': 10, 'harga': 1000
        }), content_type='application/json')
        assert response.status_code == 201

def test_pharmacist_manage_medicines_put(client):
    with patch('routes.pharmacist_routes.get_db_connection') as mock_db:
        mock_conn = mock_db.return_value
        response = client.put('/api/pharmacist/medicines', data=json.dumps({
            'id_obat': 1, 'stok': 20
        }), content_type='application/json')
        assert response.status_code == 200

def test_cashier_search_invoices(client):
    with patch('routes.cashier_routes.get_db_connection') as mock_db:
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [{'id_invoice': 1}]
        response = client.get('/api/cashier/invoices?patient_name=John')
        assert response.status_code == 200

def test_cashier_update_payment_status(client):
    with patch('routes.cashier_routes.get_db_connection') as mock_db:
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.rowcount = 1
        response = client.put('/api/cashier/invoices/1/status', data=json.dumps({
            'status_bayar': 'Lunas'
        }), content_type='application/json')
        assert response.status_code == 200
