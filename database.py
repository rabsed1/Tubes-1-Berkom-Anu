"""
Mengatur database sementara dan permanen yang berbentuk sebuah berkas csv
"""
import csv

# Membaca data dari database
def baca(path):
    with open(path, newline="", encoding="utf-8") as csvfile:
        data = csv.DictReader(csvfile)
        return list(data)

# Menulis ulang seluruh data ke database
def tulis(path, data):
    with open(path, mode="w", newline="", encoding="utf-8") as csvfile:
        fields = [*data[0]]
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

daftar_stasiun = baca("./db/stasiun.csv")
daftar_kartu = baca("./db/kartu.csv")
