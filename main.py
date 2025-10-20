stasiun_nama = ["Braga", "Cimahi", "Cimarga"]
stasiun_jarak = [0, 5, 9]
kartu_nomor = ["Ganteng676869"]
kartu_saldo = []
kartu_stasiun_masuk = [""]

# Hitung jarak dari destinasi awal ke destinasi akhir
def hitung_jarak(awal: str, akhir: str) -> int:
    indeks_awal = indeks_akhir = 0

    while(stasiun_nama[indeks_awal] != awal):
        indeks_awal += 1
    
    while(stasiun_nama[indeks_akhir] != akhir):
        indeks_akhir += 1

    jarak = abs(stasiun_jarak[indeks_akhir]-stasiun_jarak[indeks_awal])
    return jarak

# Hitung tarif berdasarkan jarak
def hitung_tarif(jarak: int) -> int:
    tarif = 3000
    
    if jarak > 25:
        tarif += (jarak - 25) * 100
    
    return tarif

# Bla
def masuk_stasiun(nomor: str, stasiun: str):
    indeks_kartu = 0
    
    while indeks_kartu < len(kartu_nomor):
        if kartu_nomor[indeks_kartu] == nomor:
            break
        indeks_kartu += 1
    
    if indeks_kartu == len(kartu_nomor):
        # Nanti diganti
        raise "Gak ada le"
    
    # if kartu_stasiun_masuk[indeks_kartu]:
    #     # Nanti diganti
    #     raise "Udah masuk woy"
    
    kartu_stasiun_masuk[indeks_kartu] = stasiun

# Bla
def keluar_stasiun(nomor: str, stasiun: str):
    indeks_kartu = 0
    
    while indeks_kartu < len(kartu_nomor):
        if kartu_nomor[indeks_kartu] == nomor:
            break
        indeks_kartu += 1
    
    if indeks_kartu == len(kartu_nomor):
        # Nanti diganti
        raise "Gak ada kartu woi"
    
    jarak = hitung_jarak(kartu_stasiun_masuk[indeks_kartu], stasiun)
    tarif = hitung_tarif(jarak)
    
    if kartu_saldo[indeks_kartu] < tarif:
        raise "Top up dulu woiii"
    
    kartu_saldo[indeks_kartu] -= tarif
    kartu_stasiun_masuk[indeks_kartu] = ""


print(hitung_tarif(hitung_jarak("Braga", "Cimarga")))