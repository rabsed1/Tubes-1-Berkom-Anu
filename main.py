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
waktu_tempuh_total = 0
jarak_tempuh_total = 0
status_pembayaran = None


# =============== Tahap 1: Tap-in ===============
while True:
    print(
        f"=" * 40,
        helper.TC_TEBAL + "CLS™ oleh KA-ITB".center(40) + helper.TUTUP,
        f" ",
        f"Versi    : 2.1-10a (LTS)",
        f"Lisensi  : GPL-3.0-only",
        f"Gerbang  : 1 (In)",
        f"=" * 40,
        sep="\n"
    )

    id_kartu = input("ID Kartu Tap-in: ")
    data_kartu = helper.cari(database.daftar_kartu, "ID", id_kartu)

    # Jika ID yang diberikan tidak valid
    # Gerbang tidak akan terbuka
    if len(id_kartu) != 10 or id_kartu != id_kartu.upper():
        print(f"\n{helper.TC_MERAH}ID yang dimasukkan tidak valid!{helper.TUTUP}")
        helper.tunggu(0.8)
        helper.bersihkan_layar()
        continue

    # Jika kartu tidak ada di daftar kartu -> kartu kedaluwarsa
    # Gerbang tidak akan terbuka
    if not data_kartu:
        print(f"\n{helper.TC_MERAH}Kartu sudah kedaluwarsa!{helper.TUTUP}")
        helper.tunggu(0.8)
        helper.bersihkan_layar()
        continue
    
    helper.simulasi_progress("Sedang mengambil data", 3)

    helper.bersihkan_layar()
    break


# =============== Tahap 2: Penentuan tujuan dan arah ===============
while True:
    # Menampilkan data kartu ke log
    print(
        f"=" * 40,
        helper.TC_TEBAL + "DATA KARTU".center(40) + helper.TUTUP,
        f" ",
        f"ID    : {data_kartu["ID"]}",
        f"Nama  : {data_kartu["Nama"]}",
        f"Saldo : Rp{int(data_kartu["Saldo"]):,}".replace(",","."),
        f"=" * 40,
        sep="\n"
    )

    # Menentukan stasiun awal dan arah kereta
    # Harusnya, hal ini dilakukan secara otomatis oleh sistem di stasiun
    stasiun_awal = input("Stasiun awal (nama): ")
    arah_kereta = input("Arah kereta (-1 atau 1): ")

    # Jika stasiun gagal memberikan:
    #   1. stasiun_awal tidak ditentukan
    #   2. arah_kereta tidak ada
    #   3. arah_kereta bukan -1 atau 1
    # Gerbang akan menampilkan error yang mencetak: "Panggil petugas"
    if not stasiun_awal or (arah_kereta != "-1" and arah_kereta != "1"):
        print(f"\n{helper.TC_MERAH}Sistem error! (panggil petugas){helper.TUTUP}")
        helper.tunggu(0.8)
        helper.bersihkan_layar()
        continue

    data_stasiun_awal = helper.cari(database.daftar_stasiun, "Nama", stasiun_awal)
    
    # Menentukan apakah arah dan stasiun tempat penumpang naik valid.
    # Tidak valid jika:
    #   1. stasiun tempat penumpang naik tidak ada
    #   2. naik di stasiun penghujung awal, tetapi arah -1
    #   3. naik di stasiun penghujung akhir, tetapi arah 1
    arah_dan_stasiun_valid = data_stasiun_awal and \
        (data_stasiun_awal["Indeks"] != "1" or arah_kereta != "-1") and \
        (data_stasiun_awal["Indeks"] != str(len(database.daftar_stasiun)) or arah_kereta != "1")
    
    # Jika tidak valid,
    # Gerbang akan menampilkan error yang mencetak: "Panggil petugas"
    if not arah_dan_stasiun_valid:
        print(f"\n{helper.TC_MERAH}Sistem error! (panggil petugas){helper.TUTUP}")
        helper.tunggu(0.8)
        helper.bersihkan_layar()
        continue

    arah_kereta = int(arah_kereta)

    helper.tunggu(1)
    helper.bersihkan_layar()
    break


# =============== Tahap 3: Simulasi tracking perjalanan ===============
id_stasiun_ujung_awal = database.daftar_stasiun[0]["ID"]
id_stasiun_ujung_akhir = database.daftar_stasiun[-1]["ID"]
start = end = 0 # Indeks stasiun naik dan penghujung rute

# Setup nilai start dan end, dan pesan arah_kereta_dari_stasiun
# Ada 2 kasus:
#   1. Jika arah_kereta == 1: start < end
#   2. Jika arah_kereta == -1: start > end
if arah_kereta == 1:
    arah_kereta_dari_stasiun = f"{id_stasiun_ujung_awal}-{id_stasiun_ujung_akhir}"
    start = int(data_stasiun_awal["Indeks"]) - 1
    end = len(database.daftar_stasiun) - 1
else:
    arah_kereta_dari_stasiun = f"{id_stasiun_ujung_akhir}-{id_stasiun_ujung_awal}"
    start = int(data_stasiun_awal["Indeks"]) - 1
    end = 0

indeks_sekarang = start

while indeks_sekarang != end:
    # Hulu = dari, hilir = ke
    stasiun_hulu = database.daftar_stasiun[indeks_sekarang]
    stasiun_hilir = database.daftar_stasiun[indeks_sekarang+arah_kereta]

    # Menghitung waktu tempuh antarstasiun dan waktu tempuh total
    # Waktu tempuh antarstasiun = jarak * 7 menit
    waktu_tempuh = stasiun.hitung_jarak(stasiun_hulu["Nama"], stasiun_hilir["Nama"]) * 7
    waktu_tempuh_total += waktu_tempuh

    # Countdown
    while waktu_tempuh > 0:
        print(
            f"=" * 40,
            f"{stasiun_hulu["Nama"]} --> {stasiun_hilir["Nama"]}".center(40),
            f"Sedang dalam perjalanan...".center(40),
            f" ",
            f"arah kereta: {arah_kereta_dari_stasiun} {' '*20}",
            f"sampai dalam: {waktu_tempuh:.1f} menit    ".replace(".",","),
            f"=" * 40,
            sep="\n"
        )
        
        helper.tunggu(0.1)
        helper.pindah_kursor(7)
        waktu_tempuh -= 0.1

    # Tampilkan pesan kedatangan
    print(
        f"=" * 40,
        f"Telah sampai di stasiun".center(40),
        f'"{stasiun_hilir["Nama"].capitalize()}"'.center(40),
        f" ",
        f" " * 40,
        f"arah kereta: {arah_kereta_dari_stasiun} {' '*20}",
        f"=" * 40,
        sep="\n"
    )

    indeks_sekarang += arah_kereta

    # Jika bukan di stasiun penghujung
    # Tanyakan ke sistem apakah penumpang sudah turun
    if indeks_sekarang - end:
        turun = input("Turun? (y/n) ")
        if turun == "y": break
    
    helper.bersihkan_layar()

# =============== Tahap 4: Turun dan Tap out ===============
# Simulasi penumpang turun dari kereta
helper.simulasi_progress("Penumpang sedang turun", 3)

helper.bersihkan_layar()
helper.pindah_kursor(8)

print(
    f"=" * 40,
    helper.TC_TEBAL + "CLS™ oleh KA-ITB".center(40) + helper.TUTUP,
    f" ",
    f"Versi    : 2.1-10a (LTS)",
    f"Lisensi  : GPL-3.0-only",
    f"Gerbang  : 3 (Out)",
    f"=" * 40,
    sep="\n"
)
helper.simulasi_progress("Sedang memproses pembayaran", 3)

# Ambil data stasiun tempat penumpang turun, jarak tempuh total, dan tarif perjlanan
data_stasiun_akhir = database.daftar_stasiun[indeks_sekarang]
jarak_tempuh_total = stasiun.hitung_jarak(data_stasiun_awal["Nama"], data_stasiun_akhir["Nama"])
tarif_perjalanan = tarif.hitung_tarif(jarak_tempuh_total)

# Jika saldo tidak cukup, atau dengan kata lain saldo < tarif,
# Gerbang tidak akan terbuka, dan mencetak pesan: "Saldo tidak cukup"
if tarif_perjalanan > int(data_kartu["Saldo"]):
    status_pembayaran = helper.TC_MERAH + "Gagal!" + helper.TUTUP
else:
    # Jika tidak, update saldo pengguna yang telah dikurangi dengan tarif ke database
    indeks_kartu = int(data_kartu["Indeks"]) - 1
    database.daftar_kartu[indeks_kartu]["Saldo"] = int(data_kartu["Saldo"]) - tarif_perjalanan
    database.tulis("./db/kartu.csv", database.daftar_kartu)
    status_pembayaran = helper.TC_HIJAU + "Suskes!" + helper.TUTUP

# Tampilkan historis perjalanan penumpang
helper.bersihkan_layar()

print(
    f"=" * 50,
    helper.TC_TEBAL + "DATA PERJALANAN".center(50) + helper.TUTUP,
    f" ",
    f"Waktu turun   : {helper.waktu_saat_ini()}",
    f"Stasiun turun : {data_stasiun_akhir["Nama"]} ({data_stasiun_akhir["ID"]})",
    f"Jarak tempuh  : {jarak_tempuh_total} km",
    f"Waktu tempuh  : {waktu_tempuh_total} menit",
    f"Tarif         : Rp{int(tarif_perjalanan):,}".replace(",","."),
    f"Pembayaran    : {status_pembayaran}",
    f"=" * 50,
    sep="\n"
)

# Konfirmasi keluar dari program
Konfirmasi_keluar = input("Pencet apapun untuk keluar...")