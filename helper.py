from time import sleep

# Cari stasiun
def cari(daftar, kunci, target):
    for item in daftar:
        if item[kunci] == target:
            return item
    
    return None

# Membersihkan layar
def bersihkan_layar():
    print("\033c", end="")

# Membuat jeda
def tunggu(detik):
    sleep(detik)
