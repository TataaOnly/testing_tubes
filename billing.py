def calculate_billing(biaya_dasar, biaya_obat, tipe_kamar):
    if not isinstance(biaya_dasar, (int, float)) or not isinstance(biaya_obat, (int, float)):
        raise TypeError("Biaya harus berupa angka.")
    
    if biaya_dasar < 0 or biaya_obat < 0:
        raise ValueError("Biaya tidak boleh negatif.")

    # Menangani tipe kamar (White Box - Branching)
    if tipe_kamar == "VIP":
        biaya_kamar = biaya_dasar * 2.0
    elif tipe_kamar == "Standar":
        biaya_kamar = biaya_dasar * 1.2
    else:
        # Menangani tipe kamar yang tidak dikenal atau tidak terdaftar
        raise ValueError(f"Tipe kamar '{tipe_kamar}' tidak terdaftar dalam sistem.")

    return biaya_kamar + biaya_obat