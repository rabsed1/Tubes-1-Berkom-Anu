from time import sleep
from datetime import datetime

BC_UNGU = '\033[45m'
BC_BIRU = '\033[44m'
BC_CYAN = '\033[46m'
BC_HIJAU = '\033[42m'
BC_KUNING = '\033[43m'
BC_MERAH = '\033[41m'
BC_ABU = '\033[40m'
TC_UNGU = '\033[95m'
TC_BIRU = '\033[94m'
TC_CYAN = '\033[96m'
TC_HIJAU = '\033[92m'
TC_KUNING = '\033[93m'
TC_MERAH = '\033[91m'
TC_TEBAL = '\033[1m'
TUTUP = '\033[0m'

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

# Ambil waktu saat ini
def waktu_saat_ini():
    return str(datetime.today().strftime("%H:%M:%S WIB, %d-%m-%Y"))

# Simulasikan progress
def simulasi_progress(tulisan, waktu):
    waktu_turun = waktu
    i = 0
    while waktu_turun >= 0:
        print(f"{tulisan}{'.' * (i % 4 + 1)} {'' * 5}")
        pindah_kursor(1)
        tunggu(0.5)
        waktu_turun -= 0.5
        i += 1