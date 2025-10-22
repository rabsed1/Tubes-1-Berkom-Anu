from os import system as os_system, name as os_name
from time import sleep

# Cari stasiun
def cari(daftar, kunci, target):
    for item in daftar:
        if item[kunci] == target:
            return item
    
    return None

# Membersihkan layar
def bersihkan_layar():
    if os_name == "nt":
        os_system("cls")
    else:
        os_system("clear")

# Membuat jeda
def tunggu(detik):
    sleep(detik)