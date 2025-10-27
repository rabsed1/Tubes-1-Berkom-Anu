"""
Menghitung tarif dan menghandle saldo
"""
from helper import cari
from database import daftar_kartu
from stasiun import hitung_jarak

# Menghitung tarif dari jarak yang diberikan
def hitung_tarif(jarak):
    tarif = 3000 
    if jarak > 25:
        tarif += (jarak - 25) * 100 
    return tarif

# Melakukan Top-Up
def top_up(id_kartu, nominal):
    kartu = cari(daftar_kartu, "ID", id_kartu)

    if not kartu:
        raise "Kartu tidak ditemukan!"
    
    kartu["Saldo"] += nominal
