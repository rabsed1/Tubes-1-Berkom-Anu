"""
Menghitung jarak dan keeping track penumpang
"""
from helper import cari
from database import daftar_kartu, daftar_stasiun

# Menghitung jarak dua stasiun
def hitung_jarak(stasiun_awal, stasiun_akhir):
    data_stasiun_awal = cari(daftar_stasiun, "Nama", stasiun_awal)
    data_stasiun_akhir = cari(daftar_stasiun, "Nama", stasiun_akhir)
    jarak_awal = int(data_stasiun_awal["Jarak"])
    jarak_akhir = int(data_stasiun_akhir["Jarak"])
    jarak = jarak_akhir - jarak_awal

    return jarak if jarak_akhir > jarak_awal else -jarak
