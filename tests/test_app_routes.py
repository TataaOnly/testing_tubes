import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Sistem Informasi Manajemen Rumah Sakit' in rv.data

def test_api_generate_billing_success(client):
    """Test the billing API with a valid appointment."""
    response = client.post('/api/billing', json={'id_appointment': 1})
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['message'] == 'Billing berhasil dibuat'
    assert 'data' in json_data
    assert json_data['data']['jenis_pembayaran'] == 'Umum'

def test_api_generate_billing_not_found(client):
    """Test the billing API with a non-existent appointment."""
    response = client.post('/api/billing', json={'id_appointment': 999})
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['error'] == 'Appointment tidak ditemukan'

def test_api_generate_billing_missing_id(client):
    """Test the billing API with missing id_appointment."""
    response = client.post('/api/billing', json={})
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['error'] == 'id_appointment dibutuhkan'

# --- User API Tests ---

def test_api_create_user_success(client):
    """Test creating a new user successfully."""
    # Ensure the user does not exist before testing
    # This part might need a way to clean up the database or use unique usernames for each run
    new_user = {'username': 'testuser_new', 'password': 'password', 'role': 'Dokter'}
    response = client.post('/api/users', json=new_user)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['message'] == 'User berhasil dibuat'
    # You might want to add a cleanup step to delete the created user

def test_api_create_user_existing(client):
    """Test creating a user that already exists."""
    existing_user = {'username': 'admin_simrs', 'password': 'password', 'role': 'Admin'}
    response = client.post('/api/users', json=existing_user)
    assert response.status_code == 409
    json_data = response.get_json()
    assert json_data['error'] == 'Username sudah digunakan'

def test_api_create_user_invalid_role(client):
    """Test creating a user with an invalid role."""
    invalid_role_user = {'username': 'testuser_invalid', 'password': 'password', 'role': 'InvalidRole'}
    response = client.post('/api/users', json=invalid_role_user)
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'Role tidak valid' in json_data['error']

def test_api_update_user_role_success(client):
    """Test updating a user's role successfully."""
    # Assuming user ID 1 exists
    response = client.put('/api/users/1/role', json={'role': 'Admin'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'berhasil diubah' in json_data['message']

def test_api_update_user_role_not_found(client):
    """Test updating a role for a non-existent user."""
    response = client.put('/api/users/999/role', json={'role': 'Admin'})
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['error'] == 'User tidak ditemukan'

def test_api_update_user_role_invalid_role(client):
    """Test updating a user's role with an invalid role."""
    response = client.put('/api/users/1/role', json={'role': 'InvalidRole'})
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'Role tidak valid' in json_data['error']
