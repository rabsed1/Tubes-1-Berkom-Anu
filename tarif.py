"""
Menghitung tarif dan menghandle saldo
"""
from helper import cari
from database import daftar_kartu, daftar_stasiun, daftar_dalam_perjalanan
from stasiun import hitung_jarak

# Menghitung tarif dari jarak yang diberikan
def hitung_tarif(jarak):
    tarif = 3000 + clamp(0, jarak, jarak - 25) * 100
    return tarif

# Melakukan pembayaran
def bayar(id_kartu):
    kartu = cari(daftar_kartu, "ID", id_kartu)
    status = cari(daftar_dalam_perjalanan, "ID", id_kartu)
    
    stasiun_awal = status["stasiun_in"]
    stasiun_akhir = stasiun["stasiun_out"]
    jarak = hitung_jarak(stasiun_awal, stasiun_akhir)
    tarif = hitung_tarif(jarak)

    if kartu["Saldo"] < tarif:
        raise "Saldo tidak cukup!"
    
    kartu["Saldo"] -= tarif

# Melakukan Top-Up
def top_up(id_kartu, nominal):
    kartu = cari(daftar_kartu, "ID", id_kartu)

    if not kartu:
        raise "Kartu tidak ditemukan!"
    
    kartu["Saldo"] += nominal
