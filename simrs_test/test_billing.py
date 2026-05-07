import pytest
from .billing import calculate_billing

def test_billing_vip():
    # Menguji jalur VIP: (500k * 2) + 200k = 1.2jt
    assert calculate_billing(500000, 200000, "VIP") == 1200000

def test_billing_standar():
    # Menguji jalur Standar: (500k * 1.2) + 200k = 800k
    assert calculate_billing(500000, 200000, "Standar") == 800000

def test_error_handling():
    # Menguji penanganan error (Exception) untuk input tidak valid
    with pytest.raises(ValueError):
        calculate_billing(1000, 500, "Economy")
        
def test_unregistered_room_type():
    # Menguji skenario kamar yang tidak ada di database (misal: "Ekonomi" atau "Presiden")
    with pytest.raises(ValueError) as excinfo:
        calculate_billing(500000, 200000, "Presiden")
    
    # Memastikan pesan error-nya sesuai
    assert "tidak terdaftar" in str(excinfo.value)

def test_empty_room_type():
    # Menguji jika input tipe kamar kosong
    with pytest.raises(ValueError):
        calculate_billing(500000, 200000, "")

def test_negative_cost():
    # Menguji jika input biaya negatif
    with pytest.raises(ValueError):
        calculate_billing(-500000, 200000, "VIP")
    with pytest.raises(ValueError):
        calculate_billing(500000, -200000, "VIP")

def test_invalid_cost_type():
    # Menguji jika input biaya bukan angka
    with pytest.raises(TypeError):
        calculate_billing("500000", 200000, "VIP")
    with pytest.raises(TypeError):
        calculate_billing(500000, "200000", "VIP")