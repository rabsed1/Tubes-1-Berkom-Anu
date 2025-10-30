# Program SimulasiSistemTicketingCommuterLine
# Mensimulasi tap-in, tap-out, tracking penumpang, dan pembayaran
# yang dilakukan oleh penumpang dari perspektif sistem ticketing commuter line

# Kamus
# daftar_stasiun_ID: array [0..n] of string, memuat ID unik tiap stasiun
# daftar_stasiun_NAMA: array [0..n] of string, memuat nama tiap stasiun
# daftar_stasiun_JARAK: array [0..n] of int, memuat jarak relatif dari awal rute untuk tiap stasiun
# daftar_kartu_ID: array [0..n] of string, memuat ID unik tiap kartu
# daftar_kartu_NAMA: array [0..n] of string, memuat nama pemilik tiap kartu
# daftar_kartu_SALDO: array [0..n] of int, memuat saldo tiap kartu
# jumlah_stasiun: int, memuat jumlah stasiun yang ada di database
# jumlah_kartu: int, memuat jumlah stasiun yang ada di database
# indeks_kartu: int, memuat indeks kartu yang dimasukkan ketika tap-in
# indeks_stasiun_awal: int, memuat indeks stasiun tempat penumpang naik
# indeks_stasiun_akhir: int, memuat indeks stasiun tempat penumpang turun
# indeks_stasiun_awal_rute: int, memuat indeks stasiun di awal rute
# indeks_stasiun_akhir_rute: int, memuat indeks stasiun di akhir rute
# arah_kereta: int, memuat arah kereta yang dinaiki penumpang (-1 atau 1)
# rute_kereta: string, memuat kode kereta yang dapat menunjukkan arah kereta
# waktu_tempuh_total: int, memuat waktu total yang ditempuh penumpang
# jarak_tempuh_total: int, memuat jarak total yang ditempuh penumpang
# status_pembayaran: string, memuat status pembayaran ("Gagal!" atau "Sukses!")

# Algoritma
from time import sleep as tunggu
from csv import reader as csv_baca, writer as csv_tulis
from datetime import datetime

# CONFIG DATABASE
DB_STASIUN_ENT_MAKS = 25
DB_KARTU_ENT_MAKS = 25

# CONFIG WARNA (disingkat WN)
WN_TXT_TEBAL = "\033[1m"
WN_TXT_PROC_SUKSES = "\033[92m"
WN_TXT_PROC_ERROR = "\033[91m"
WN_TUTUP_ = "\033[0m"

# CONFIG WAKTU (disingkat WK) (dalam detik)
WK_SIMUL_PROGRESS = 3
WK_SIMUL_ERROR = 0.8
WK_SIMUL_TEMPUH = 2
WK_CONTD_TRACKER = 0.1
WK_CONTD_PROGRESS = 0.5

# INISIALISASI VARIABEL GLOBAL DATABASE
daftar_stasiun_ID = [None for _ in range(DB_STASIUN_ENT_MAKS)]
daftar_stasiun_NAMA = [None for _ in range(DB_STASIUN_ENT_MAKS)]
daftar_stasiun_JARAK = [None for _ in range(DB_STASIUN_ENT_MAKS)]
daftar_kartu_ID = [None for _ in range(DB_KARTU_ENT_MAKS)]
daftar_kartu_NAMA = [None for _ in range(DB_KARTU_ENT_MAKS)]
daftar_kartu_SALDO = [None for _ in range(DB_KARTU_ENT_MAKS)]
jumlah_stasiun = 0
jumlah_kartu = 0

# INISIALISASI VARIABEL GLOBAL
indeks_kartu = None
indeks_stasiun_awal = None
indeks_stasiun_akhir = None
indeks_stasiun_awal_rute = None
indeks_stasiun_akhir_rute = None
arah_kereta = None
rute_kereta = None
waktu_tempuh_total = 0
jarak_tempuh_total = 0
status_pembayaran = None

# Pengambilan Database
with open("./kartu.csv", newline="", encoding="utf-8") as csvfile:
    daftar_kartu = list(csv_baca(csvfile))
    jumlah_kartu = len(daftar_kartu)
    jumlah_kartu = jumlah_kartu if jumlah_kartu < DB_KARTU_ENT_MAKS else DB_KARTU_ENT_MAKS

    for i in range(1, jumlah_kartu):
        daftar_kartu_ID[i-1] = daftar_kartu[i][0]
        daftar_kartu_NAMA[i-1] = daftar_kartu[i][1]
        daftar_kartu_SALDO[i-1] = int(daftar_kartu[i][2])

    jumlah_kartu -= 1

with open("./stasiun.csv", newline="", encoding="utf-8") as csvfile:
    daftar_stasiun = list(csv_baca(csvfile))
    jumlah_stasiun = len(daftar_stasiun)
    jumlah_stasiun = jumlah_stasiun if jumlah_stasiun < DB_STASIUN_ENT_MAKS else DB_STASIUN_ENT_MAKS

    for i in range(1, jumlah_stasiun):
        daftar_stasiun_ID[i-1] = daftar_stasiun[i][0]
        daftar_stasiun_NAMA[i-1] = daftar_stasiun[i][1]
        daftar_stasiun_JARAK[i-1] = int(daftar_stasiun[i][2])

    jumlah_stasiun -= 1


"""
    ==================================================================
    ====================== Tahap 1: Tap-in ===========================
    ==================================================================
"""
loop1 = True
while loop1:
    print("\033c", end="")

    # Tampilkan informasi program
    print(
        "=" * 40,
        f"{WN_TXT_TEBAL}{"CLTS™ oleh Skibidi".center(40)}{WN_TUTUP_}",
        " " * 40,   
        "Versi    : 6.7 (Dubai Chocolate)",
        "Lisensi  : Anu",
        "Gerbang  : 6 (In)",
        "=" * 40,
        sep="\n"
    )

    id_kartu = input("ID Kartu Tap-in: ")

    # Lakukan pencarian ID Kartu
    for i in range(jumlah_kartu):
        if daftar_kartu_ID[i] == id_kartu:
            indeks_kartu = i

    # Jika ID kartu tidak valid
    if len(id_kartu) != 10 or id_kartu != id_kartu.upper():
        print(f"\n{WN_TXT_PROC_ERROR}ID yang dimasukkan tidak valid!{WN_TUTUP_}")
        tunggu(WK_SIMUL_ERROR)

    # Jika ID kartu tidak ditemukan
    elif not indeks_kartu:
        print(f"\n{WN_TXT_PROC_ERROR}Kartu sudah kedaluwarsa!{WN_TUTUP_}")
        tunggu(WK_SIMUL_ERROR)
    
    # Jika ID kartu ditemukan
    else:
        # Simulasi loading
        t = WK_SIMUL_PROGRESS
        i = 0
        while t >= 0:
            print(f"Sedang mengambil data{'.' * (i%4 + 1)} {'' * 5}")
            print(f"\033[1A\033[2K", end="")
            tunggu(WK_CONTD_PROGRESS)
            t -= WK_CONTD_PROGRESS
            i += 1
        
        print("\033c", end="")
        loop1 = False


"""
    ==================================================================
    ============== Tahap 2: Penentuan tujuan dan arah ================
    ==================================================================
"""
loop2 = True
while loop2:
    print("\033c", end="")

    # Tampilkan informasi kartu
    print(
        "=" * 40,
        f"{WN_TXT_TEBAL}{"DATA KARTU".center(40)}{WN_TUTUP_}",
        " ",
        f"ID    : {daftar_kartu_ID[indeks_kartu]}",
        f"Nama  : {daftar_kartu_NAMA[indeks_kartu]}",
        f"Saldo : Rp{int(daftar_kartu_SALDO[indeks_kartu]):,}".replace(",","."),
        "=" * 40,
        sep="\n"
    )

    # Tampilkan daftar stasiun
    maks_dig = len(str(jumlah_stasiun))
    for i in range(jumlah_stasiun):
        print(
            f"{str(i+1).zfill(maks_dig)}.", 
            f"({daftar_stasiun_ID[i]})",
            f"{daftar_stasiun_NAMA[i]}"
        )

    print("\n")

    indeks_stasiun_awal = input("Stasiun awal (indeks): ").strip()
    arah_kereta = input("Arah kereta (-1 atau 1): ").strip()

    # Jika input indeks stasun kosong atau
    # arah kereta bukan "-1" atau "1"
    if not indeks_stasiun_awal or (arah_kereta != "-1" and arah_kereta != "1"):
        print(f"\n{WN_TXT_PROC_ERROR}Sistem error! (panggil petugas){WN_TUTUP_}")
        tunggu(WK_SIMUL_ERROR)
    
    # Jika input indeks stasun tidak kosong atau
    # arah kereta adalah "-1" atau "1"
    else:
        stasiun_valid = indeks_stasiun_awal.isdigit()
        indeks_stasiun_awal = int(indeks_stasiun_awal) - 1
        arah_valid = \
            (indeks_stasiun_awal != 0 or arah_kereta != "-1") and \
            (indeks_stasiun_awal != jumlah_stasiun - 1 or arah_kereta != "1")
    
        # Jika indeks stasiun tidak berupa angka atau arah kereta tidak valid
        # Arah kereta tidak valid jika:
        #  1. Dimulai di awal dan kereta mengarah ke kiri
        #  2. Dimulai di akhir dan kereta mengarah ke kanan
        if not (stasiun_valid and arah_valid):
            print(f"\n{WN_TXT_PROC_ERROR}Sistem error! (panggil petugas){WN_TUTUP_}")
            tunggu(WK_SIMUL_ERROR)
        
        # Jika indeks stasiun berupa angka atau arah kereta valid
        else:
            arah_kereta = int(arah_kereta)
            tunggu(1)
            print("\033c", end="")
            loop2 = False


"""
    ==================================================================
    ================= Tahap 3: Track perjalanan ======================
    ==================================================================
"""
# Muat indeks stasiun di awal dan akhir rute
indeks_stasiun_awal_rute = 0
indeks_stasiun_akhir_rute = jumlah_stasiun - 1

# Muat pointer dan end untuk simulasi tracking
pointer = indeks_stasiun_awal
end = (jumlah_stasiun - 1) * (arah_kereta == 1)

# Untuk menampilkan kode rute
if arah_kereta == 1:
    rute_kereta = daftar_stasiun_ID[indeks_stasiun_awal_rute]
    rute_kereta += "-"
    rute_kereta += daftar_stasiun_ID[indeks_stasiun_akhir_rute]
else:
    rute_kereta = daftar_stasiun_ID[indeks_stasiun_akhir_rute]
    rute_kereta += "-"
    rute_kereta += daftar_stasiun_ID[indeks_stasiun_awal_rute]

loop3 = True
while loop3:
    # Memuat nama stasiun hulu (dari) dan hilir (ke)
    nama_stasiun_hulu = daftar_stasiun_NAMA[pointer]
    nama_stasiun_hilir = daftar_stasiun_NAMA[pointer+arah_kereta]

    # Menghitung jarak tempuh antarstasiun
    jarak_tempuh = daftar_stasiun_JARAK[pointer+arah_kereta] - daftar_stasiun_JARAK[pointer]
    jarak_tempuh = jarak_tempuh if jarak_tempuh > 0 else -jarak_tempuh
    
    # Menghitung waktu tempuh antarstasiun
    waktu_tempuh = jarak_tempuh * WK_SIMUL_TEMPUH

    # Menghitung waktu tempuh total
    waktu_tempuh_total += waktu_tempuh

    # Lakukan tracking dengan countdown
    while waktu_tempuh > 0:
        print(
            f"=" * 40,
            f"{nama_stasiun_hulu} --> {nama_stasiun_hilir}".center(40),
            f"Sedang dalam perjalanan...".center(40),
            f" " * 40,
            f"arah kereta: {rute_kereta} {' ' * 10}",
            f"sampai dalam: {waktu_tempuh:.1f} menit {' ' * 10}".replace(".",","),
            f"=" * 40,
            sep="\n"
        )
        
        tunggu(WK_CONTD_TRACKER)
        print(f"\033[7A\033[2K", end="")
        waktu_tempuh -= WK_CONTD_TRACKER

    # Tampilkan informasi jika telah sampai
    print(
        f"=" * 40,
        f"Telah sampai di stasiun".center(40),
        f'"{nama_stasiun_hilir.capitalize()}"'.center(40),
        f" " * 40,
        f" " * 40,
        f"arah kereta: {rute_kereta} {' ' * 10}",
        f"=" * 40,
        sep="\n"
    )

    pointer += arah_kereta

    # Jika tidak berada di penghujung rute,
    # konfirmasikan apakah penumpang turun atau tidak
    if pointer - end:
        # Konfirmasi penumpang turun atau tidak
        # Hanya menerima input "y" atau "n"
        loop_input = True
        while loop_input:
            turun = input("Turun? (y/n) ").strip()
            
            # Penumpang turun
            if turun == "y":
                loop3 = False
                loop_input = False
            
            # Penumpang tidak turun
            elif turun == "n":
                print("\033c", end="")
                loop_input = False
            
            # Input tidak valid
            else:
                print(f"\033[1A\033[2K", end="")
    
    # Jika berada di penghujung rute,
    # otomatis penumpang akan turun, jadi tidak usah ditanyakan
    else:
        print("\033c", end="")
        loop3 = False


"""
    ==================================================================
    ======================== Tahap 4: Tap-out ========================
    ==================================================================
"""
# Simulasi loading
t = WK_SIMUL_PROGRESS
i = 0
while t >= 0:
    print(f"Penumpang sedang turun{'.' * (i%4 + 1)} {'' * 5}")
    print(f"\033[1A\033[2K", end="")
    tunggu(WK_CONTD_PROGRESS)
    t -= WK_CONTD_PROGRESS
    i += 1

print("\033c", end="")
print(f"\033[8A\033[2K", end="")

# Tampilkan informasi sistem
print(
    "=" * 40,
    f"{WN_TXT_TEBAL}{"CLTS™ oleh Skibidi".center(40)}{WN_TUTUP_}",
    " " * 40,   
    "Versi    : 6.7 (Dubai Chocolate)",
    "Lisensi  : Anu",
    "Gerbang  : 7 (Out)",
    "=" * 40,
    sep="\n"
)

# Simulasi loading
t = WK_SIMUL_PROGRESS
i = 0
while t >= 0:
    print(f"Sedang memproses pembayaran{'.' * (i%4 + 1)} {'' * 5}")
    print(f"\033[1A\033[2K", end="")
    tunggu(WK_CONTD_PROGRESS)
    t -= WK_CONTD_PROGRESS
    i += 1


"""
    ==================================================================
    =================== Tahap 5: Penampilan Histori ==================
    ==================================================================
"""
# Tetapkan indeks stasiun akhir
indeks_stasiun_akhir = pointer

# Hitung jarak tempuh total (dan normalisasi, tanpa menggunakan abs())
jarak_tempuh_total = daftar_stasiun_JARAK[indeks_stasiun_akhir] - daftar_stasiun_JARAK[indeks_stasiun_awal]
jarak_tempuh_total = jarak_tempuh_total if jarak_tempuh_total > 0 else -jarak_tempuh_total

# Hitung tarif perjalanan
tarif_perjalanan = 3000
tarif_perjalanan += (jarak_tempuh_total - 25) * 100 if jarak_tempuh_total > 25 else 0

# Jika saldo tidak cukup
if tarif_perjalanan > int(daftar_kartu_SALDO[indeks_kartu]):
    status_pembayaran = WN_TXT_PROC_ERROR + "Gagal!" + WN_TUTUP_

# Jika saldo cukup
else:
    daftar_kartu_SALDO[indeks_kartu] -= tarif_perjalanan
    status_pembayaran = WN_TXT_PROC_SUKSES + "Suskes!" + WN_TUTUP_

    # Update informasi baru ke database
    with open("./kartu.csv", mode="w", newline="", encoding="utf-8") as csvfile:
        fields = ["ID", "Nama", "Saldo"]
        writer = csv_tulis(csvfile)
        writer.writerow(fields)

        for i in range(jumlah_kartu):
            writer.writerow([
                daftar_kartu_ID[i],
                daftar_kartu_NAMA[i],
                daftar_kartu_SALDO[i]
            ])
    
print("\033c", end="")

# Tampilkan historis perjalanan
print(
    f"=" * 50,
    f"{WN_TXT_TEBAL}{"DATA PERJALANAN".center(50)}{WN_TUTUP_}",
    f" " * 50,
    f"Waktu turun   : {str(datetime.today().strftime("%H:%M:%S WIB, %d-%m-%Y"))}",
    f"Stasiun naik  : {daftar_stasiun_NAMA[indeks_stasiun_awal]} ({daftar_stasiun_ID[indeks_stasiun_awal]})",
    f"Stasiun turun : {daftar_stasiun_NAMA[indeks_stasiun_akhir]} ({daftar_stasiun_ID[indeks_stasiun_akhir]})",
    f"Jarak tempuh  : {jarak_tempuh_total} km",
    f"Waktu tempuh  : {waktu_tempuh_total} menit",
    f"Tarif         : Rp{int(tarif_perjalanan):,}".replace(",","."),
    f"Pembayaran    : {status_pembayaran}",
    f"=" * 50,
    sep="\n"
)

# Konfirmasi keluar program
input("Pencet apapun untuk keluar...")