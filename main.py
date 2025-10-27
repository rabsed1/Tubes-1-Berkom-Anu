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
kartu_penumpang = None

while True:
    id_penumpang = input("Silakan masukkan ID kartu Anda: ")
    kartu_penumpang = helper.cari(database.daftar_kartu, "ID", id_penumpang)

    if len(id_penumpang) != 10 or id_penumpang != id_penumpang.upper():
        print("ID yang dimasukkan tidak valid!")
        continue

    if not kartu_penumpang:
        print("\nMaaf, kartu Tidak Terdaftar!")
        helper.tunggu(0.8)
        helper.bersihkan_layar()
        continue
    
    break

helper.bersihkan_layar()
print(
    f"ID: {kartu_penumpang["ID"]}\n",
    f"Nama: {kartu_penumpang["Nama"]}\n",
    f"Saldo: Rp{int(kartu_penumpang["Saldo"]):,}".replace(",","."),
    sep=""
)

print("\n")
    