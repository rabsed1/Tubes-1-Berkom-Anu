from time import sleep

# Cari dari daftar (list of dictionaries)
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

# Memindah kursor stdout
def pindah_kursor(baris):
    print(f"\033[{baris}A\033[2K", end="")