"""
Entry-point aplikasi
"""
if __name__ != "__main__":
    raise "Harus dijalankan secara langsung!"

import stasiun
import tarif
import helper
import database

helper.bersihkan_layar()
data_kartu = None
data_stasiun_awal = None
data_stasiun_akhir = None
arah_kereta = None
arah_kereta_dari_stasiun = None
waktu_tempuh = 0
jarak_tempuh = 0

while True:
    # id_kartu = input("ID Kartu Tap-in: ")
    id_kartu = "AAAAAAAAAA"
    data_kartu = helper.cari(database.daftar_kartu, "ID", id_kartu)

    if len(id_kartu) != 10 or id_kartu != id_kartu.upper():
        print("ID yang dimasukkan tidak valid!") # Gerbang tidak dibuka, error ditampilkan
        helper.tunggu(0.8)
        helper.bersihkan_layar()
        continue

    if not data_kartu:
        print("\nMaaf, kartu sudah kadaluwarsa!") # Gerbang tidak dibuka, error ditampilkan
        helper.tunggu(0.8)
        helper.bersihkan_layar()
        continue
    
    # helper.bersihkan_layar()
    break

while True:
    print(
        f"=" * 40,
        f"DATA KARTU".center(40),
        f" ",
        f"ID    : {data_kartu["ID"]}",
        f"Nama  : {data_kartu["Nama"]}",
        f"Saldo : Rp{int(data_kartu["Saldo"]):,}".replace(",","."),
        f"=" * 40,
        sep="\n"
    )

    stasiun_awal = input("Stasiun awal (nama): ")
    arah_kereta = input("Arah kereta (-1 atau 1): ")

    if not stasiun_awal or (arah_kereta != "-1" and arah_kereta != "1"):
        print("\nSistem error! (silakan coba lagi atau panggil petugas)") # Harusnya tidak error
        helper.tunggu(0.8)
        helper.bersihkan_layar()
        continue
    
    data_stasiun_awal = helper.cari(database.daftar_stasiun, "Nama", stasiun_awal)

    if not data_stasiun_awal:
        print("\nSistem error! (silakan coba lagi atau panggil petugas)") # Harusnya tidak error
        helper.tunggu(0.8)
        helper.bersihkan_layar()
        continue

    if data_stasiun_awal["Indeks"] == "1" and arah_kereta == "-1":
        print("\nSistem error! (silakan coba lagi atau panggil petugas)") # Harusnya tidak error
        helper.tunggu(0.8)
        helper.bersihkan_layar()
        continue

    if data_stasiun_awal["Indeks"] == len(database.daftar_stasiun) + 1 and arah_kereta == "1":
        print("\nSistem error! (silakan coba lagi atau panggil petugas)") # Harusnya tidak error
        helper.tunggu(0.8)
        helper.bersihkan_layar()
        continue

    arah_kereta = int(arah_kereta)

    helper.tunggu(1)
    helper.bersihkan_layar()
    break

id_stasiun_ujung_awal = database.daftar_stasiun[0]["ID"]
id_stasiun_ujung_akhir = database.daftar_stasiun[-1]["ID"]
start = end = 0

if arah_kereta == 1:
    arah_kereta_dari_stasiun = f"{id_stasiun_ujung_awal}-{id_stasiun_ujung_akhir}"
    start = int(data_stasiun_awal["Indeks"]) - 1
    end = len(database.daftar_stasiun) - 1
else:
    arah_kereta_dari_stasiun = f"{id_stasiun_ujung_akhir}-{id_stasiun_ujung_awal}"
    start = int(data_stasiun_awal["Indeks"]) - 1
    end = 0

i = start
while i != end:
    stasiun_hulu = database.daftar_stasiun[i]
    stasiun_hilir = database.daftar_stasiun[i+arah_kereta]

    t = stasiun.hitung_jarak(stasiun_hulu["Nama"], stasiun_hilir["Nama"]) * 7
    waktu_tempuh += t

    while t > 0:
        print(
            f"=" * 40,
            f"{stasiun_hulu["Nama"]} --> {stasiun_hilir["Nama"]}".center(40),
            f"Sedang dalam perjalanan...".center(40),
            f"{i} {end}",
            f"arah kereta: {arah_kereta_dari_stasiun}              ",
            f"sampai dalam: {t:.1f} menit    ".replace(".",","),
            f"=" * 40,
            sep="\n"
        )
        
        helper.tunggu(0.1)
        print("\033[7A\033[2K", end="")
        t -= 0.1

    print(
        f"=" * 40,
        f"Telah sampai di stasiun".center(40),
        f'"{stasiun_hilir["Nama"].capitalize()}"'.center(40),
        f" ",
        f" " * 40,
        f"arah kereta: {arah_kereta_dari_stasiun}              ",
        f"=" * 40,
        sep="\n"
    )

    i += arah_kereta

    if i-end:
        turun = input("Turun? (y/n) ")

        if turun == "y": 
            helper.bersihkan_layar()
            break
    
    helper.bersihkan_layar()

data_stasiun_akhir = database.daftar_stasiun[i]
jarak_tempuh = stasiun.hitung_jarak(data_stasiun_awal["Nama"], data_stasiun_akhir["Nama"])
tarif_perjalanan = tarif.hitung_tarif(jarak_tempuh)

if tarif_perjalanan > int(data_kartu["Saldo"]):
    print("\nSaldo tidak cukup!\n") # Waduh bokek
    helper.tunggu(0.8)
    raise

print(
    f"=" * 40,
    f"DATA PERJALANAN".center(40),
    f" ",
    f"Stasiun turun : {data_stasiun_akhir["Nama"]} ({data_stasiun_akhir["ID"]})",
    f"Jarak tempuh  : {jarak_tempuh} km",
    f"Waktu tempuh  : {waktu_tempuh} menit",
    f"Tarif         : Rp{int(tarif_perjalanan):,}".replace(",","."),
    f"=" * 40,
    sep="\n"
)

indeks_kartu = int(data_kartu["Indeks"]) - 1
database.daftar_kartu[indeks_kartu]["Saldo"] = int(data_kartu["Saldo"]) - tarif_perjalanan
database.tulis("./db/kartu.csv", database.daftar_kartu)