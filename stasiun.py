"""
Menghitung jarak dan keeping track penumpang
"""
from helper import cari
from database import daftar_kartu, daftar_stasiun, daftar_dalam_perjalanan

# Menghitung jarak dua stasiun
def hitung_jarak(stasiun_awal, stasiun_akhir):
    data_stasiun_awal = cari(daftar_stasiun, "Nama", stasiun_awal)
    data_stasiun_akhir = cari(daftar_stasiun, "Nama", stasiun_akhir)
    jarak_awal = data_stasiun_awal["Jarak"]
    jarak_akhir = data_stasiun_akhir["Jarak"]

    return abs(jarak_akhir - jarak_awal)

# Mengatur destinasi awal untuk kartu yang diberikan
def masuk_stasiun(id_kartu, nama_stasiun):
    kartu = cari(daftar_kartu, "ID", id_kartu)
    
    if not kartu:
        raise "Kartu tidak ditemukan!"
    
    daftar_dalam_perjalanan.append({
        "ID": kartu["ID"],
        "stasiun_in": nama_stasiun,
        "stasiun_out": ""
    })

# Mengatur destinasi keluar untuk kartu yang diberikan
def keluar_stasiun(id_kartu, nama_stasiun):
    kartu = cari(daftar_kartu, "ID", id_kartu)

    if not kartu:
        raise "Kartu tidak ditemukan!"
    
    for penumpang in daftar_dalam_perjalanan:
        if penumpang["ID"] == id_kartu:
            penumpang["stasiun_out"] = nama_stasiun
    
    # Handler galatnya nggak?

# Menghapus penumpang yang sedang dalam perjalanan
def hapus_status_dalam_perjalanan(id_kartu):
    for i in range(len(daftar_dalam_perjalanan)):
        if daftar_dalam_perjalanan[i]["ID"] == id_kartu:
            del daftar_dalam_perjalanan[i]
            return True
    
    return False
