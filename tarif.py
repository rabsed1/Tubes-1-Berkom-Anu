"""
Menghitung tarif dan menghandle saldo
"""
from helper import cari
from stasiun import hitung_jarak

# Menghitung tarif dari jarak yang diberikan
def hitung_tarif(jarak):
    tarif = 3000 * bool(jarak)
    if jarak > 25:
        tarif += (jarak - 25) * 100 
    return tarif
