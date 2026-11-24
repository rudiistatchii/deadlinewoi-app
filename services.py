"""
services.py — Modul logika bisnis (Service Layer) aplikasi DeadlineWoi.

Modul ini bertindak sebagai perantara antara lapisan penyimpanan (storage.py)
dan lapisan antarmuka (ui.py / main.py). 

Sesuai prinsip pemrograman modular, logika pengolahan data tidak boleh ditaruh
di UI atau penyimpanan file, melainkan diatur di modul ini.

Fitur lanjutan yang diterapkan:
- Penerapan OOP: Class TugasService
- Konsep *args   : Perhitungan agregasi total jam tugas dinamis
- Konsep **kwargs : Penyaringan (filtering) data secara variatif
- Penggunaan lambda : Kunci kustom pada algoritma pengurutan (sorting)
- Algoritma pencarian : Pencarian substring case-insensitive pada data
"""

import os
from typing import List, Optional

from models import Tugas
import storage
import validasi


class TugasService:
    """
    Class pengelola data dan logika bisnis tugas kuliah.

    Atribut
    -------
    path_csv     : str         — Lokasi file CSV tempat data disimpan.
    daftar_tugas : list[Tugas] — Koleksi objek Tugas di dalam memori RAM.
    """

    def __init__(self, path_csv: Optional[str] = None) -> None:
        """
        Inisialisasi TugasService dan memuat data tugas dari CSV.

        Parameter
        ---------
        path_csv : Path ke file CSV. Jika None, otomatis menggunakan
                   'data/tugas.csv' relatif terhadap direktori modul ini.
        """
        if path_csv is None:
            folder_ini = os.path.dirname(os.path.abspath(__file__))
            self.path_csv = os.path.join(folder_ini, "data", "tugas.csv")
        else:
            self.path_csv = path_csv

        self.daftar_tugas: List[Tugas] = []
        self.muat()

    # ------------------------------------------------------------------ #
    #  Operasi Dasar (CRUD & Sinkronisasi Penyimpanan)
    # ------------------------------------------------------------------ #

    def muat(self) -> List[Tugas]:
        """
        Muat ulang seluruh tugas dari file CSV ke dalam memori.

        Return
        ------
        List objek Tugas terbaru.
        """
        self.daftar_tugas = storage.muat_data(self.path_csv)
        return self.daftar_tugas

    def simpan(self) -> None:
        """Tulis ulang seluruh data tugas dari memori ke file CSV."""
        storage.simpan_data(self.path_csv, self.daftar_tugas)

    def ambil_semua(self) -> List[Tugas]:
        """
        Ambil seluruh daftar tugas yang sedang aktif di memori.

        Return
        ------
        List salinan dari objek Tugas.
        """
        return list(self.daftar_tugas)

    def ambil_berdasarkan_id(self, id_tugas: str) -> Optional[Tugas]:
        """
        Cari satu tugas berdasarkan kode ID uniknya.

        Parameter
        ---------
        id_tugas : String ID tugas, misalnya 'T001'.

        Return
        ------
        Objek Tugas jika ditemukan, atau None jika tidak ada.
        """
        id_target = id_tugas.strip().upper()
        for tugas in self.daftar_tugas:
            if tugas.id.upper() == id_target:
                return tugas
        return None

    def buat_id_otomatis(self) -> str:
        """
        Generate ID baru secara urut (contoh: T021 jika ada 20 data).

        Return
        ------
        String ID baru dengan format 'T' diikuti 3 digit angka.
        """
        angka_maks = 0
        for tugas in self.daftar_tugas:
            # Ambil digit angka di belakang huruf T (contoh 'T005' -> 5)
            if tugas.id.startswith("T") and tugas.id[1:].isdigit():
                angka = int(tugas.id[1:])
                if angka > angka_maks:
                    angka_maks = angka
        return f"T{angka_maks + 1:03d}"

    def tambah_tugas(self, data_input: dict) -> Tugas:
        """
        Validasi dan tambahkan satu tugas baru ke sistem dan CSV.

        Parameter
        ---------
        data_input : Dictionary data mentah (misal dari form input pengguna).

        Return
        ------
        Objek Tugas yang baru dibuat dan disimpan.

        Raises
        ------
        ValueError : Jika input melanggar aturan validasi atau ID duplikat.
        """
        # 1. Jika ID tidak disertakan, buatkan ID otomatis
        if "id" not in data_input or not data_input["id"].strip():
            data_input["id"] = self.buat_id_otomatis()

        # 2. Cek apakah ID sudah dipakai sebelumnya
        if self.ambil_berdasarkan_id(data_input["id"]) is not None:
            raise ValueError(f"Tugas dengan ID '{data_input['id']}' sudah ada.")

        # 3. Validasi seluruh data menggunakan validasi.py
        data_valid = validasi.validasi_semua(data_input)

        # 4. Buat objek Tugas baru
        tugas_baru = Tugas.dari_dict(data_valid)

        # 5. Tambahkan ke memori dan simpan permanen
        self.daftar_tugas.append(tugas_baru)
        storage.tambah_baris(self.path_csv, tugas_baru)

        return tugas_baru

    def hapus_tugas(self, id_tugas: str) -> bool:
        """
        Hapus tugas dari daftar berdasarkan ID.

        Parameter
        ---------
        id_tugas : ID tugas yang ingin dihapus.

        Return
        ------
        True jika berhasil dihapus, False jika ID tidak ditemukan.
        """
        tugas = self.ambil_berdasarkan_id(id_tugas)
        if tugas is None:
            return False

        self.daftar_tugas.remove(tugas)
        self.simpan()
        return True

    def perbarui_status(self, id_tugas: str, status_baru: str) -> Tugas:
        """
        Perbarui status pengerjaan suatu tugas.

        Parameter
        ---------
        id_tugas    : ID tugas yang statusnya ingin diubah.
        status_baru : Status baru ('Belum', 'Proses', 'Selesai').

        Return
        ------
        Objek Tugas yang sudah diperbarui.

        Raises
        ------
        ValueError : Jika ID tidak ditemukan atau status baru tidak sah.
        """
        status_valid = validasi.validasi_status(status_baru)
        tugas = self.ambil_berdasarkan_id(id_tugas)

        if tugas is None:
            raise ValueError(f"Tugas dengan ID '{id_tugas}' tidak ditemukan.")

        tugas.status = status_valid
        self.simpan()
        return tugas

    # ------------------------------------------------------------------ #
    #  Algoritma Pencarian & Pengurutan (Searching & Sorting)
    # ------------------------------------------------------------------ #

    def cari_tugas(self, kata_kunci: str, kolom: str = "semua") -> List[Tugas]:
        """
        Mencari tugas yang mengandung kata kunci (metode Linear Search).

        Parameter
        ---------
        kata_kunci : Teks pencarian (case-insensitive).
        kolom      : Bidang pencarian ('judul', 'mata_kuliah', 'kategori', 'id', 'semua').

        Return
        ------
        List objek Tugas yang cocok dengan kata kunci.
        """
        kunci = kata_kunci.strip().lower()
        if not kunci:
            return self.ambil_semua()

        hasil: List[Tugas] = []
        for tugas in self.daftar_tugas:
            cocok = False
            if kolom == "judul":
                cocok = kunci in tugas.judul.lower()
            elif kolom == "mata_kuliah":
                cocok = kunci in tugas.mata_kuliah.lower()
            elif kolom == "kategori":
                cocok = kunci in tugas.kategori.lower()
            elif kolom == "id":
                cocok = kunci in tugas.id.lower()
            else:  # "semua" kolom teks
                cocok = (
                    kunci in tugas.judul.lower()
                    or kunci in tugas.mata_kuliah.lower()
                    or kunci in tugas.kategori.lower()
                    or kunci in tugas.id.lower()
                )

            if cocok:
                hasil.append(tugas)

        return hasil

    def urutkan_tugas(
        self,
        daftar: Optional[List[Tugas]] = None,
        kunci: str = "deadline",
        menurun: bool = False,
    ) -> List[Tugas]:
        """
        Mengurutkan daftar tugas menggunakan lambda function (Sorting).

        Parameter
        ---------
        daftar  : List tugas yang ingin diurutkan (jika None, pakai self.daftar_tugas).
        kunci   : Atribut pengurutan ('deadline', 'prioritas', 'bobot_jam', 'judul').
        menurun : True untuk Descending (Z-A / terbesar dulu), False untuk Ascending.

        Return
        ------
        List tugas yang sudah terurut.
        """
        target = self.daftar_tugas if daftar is None else daftar

        # Pemetaan ekspresi lambda berdasarkan atribut pengurutan
        peta_kunci = {
            "deadline": lambda t: t.deadline,
            "prioritas": lambda t: t.prioritas,
            "bobot_jam": lambda t: t.bobot_jam,
            "judul": lambda t: t.judul.lower(),
            "mata_kuliah": lambda t: t.mata_kuliah.lower(),
        }

        fungsi_kunci = peta_kunci.get(kunci, lambda t: t.deadline)

        # Pengurutan data menggunakan sorted() dan lambda
        return sorted(target, key=fungsi_kunci, reverse=menurun)

    # ------------------------------------------------------------------ #
    #  Fitur Lanjutan: *args (Agregasi Data) & **kwargs (Filter Fleksibel)
    # ------------------------------------------------------------------ #

    def hitung_total_jam(self, *tugas_pilihan: Tugas) -> float:
        """
        Menghitung total estimasi jam pengerjaan menggunakan *args.

        Parameter
        ---------
        *tugas_pilihan : Kumpulan positional arguments berupa objek Tugas.
                         Jika tidak ada argumen yang dikirimkan, fungsi otomatis
                         menghitung seluruh tugas yang ada di sistem.

        Return
        ------
        Total jam pengerjaan (float).
        """
        # Jika *args kosong, gunakan seluruh tugas yang ada di memori
        kumpulan_tugas = tugas_pilihan if tugas_pilihan else self.daftar_tugas
        return sum(t.bobot_jam for t in kumpulan_tugas)

    def filter_tugas(self, **kriteria) -> List[Tugas]:
        """
        Menyaring daftar tugas secara dinamis menggunakan **kwargs.

        Contoh penggunaan:
            service.filter_tugas(status="Belum")
            service.filter_tugas(prioritas=1, kategori="Proyek")

        Parameter
        ---------
        **kriteria : Keyword arguments atribut yang dicocokkan
                     (misal status='Proses', prioritas=1, kategori='Kuis').

        Return
        ------
        List objek Tugas yang memenuhi seluruh kriteria.
        """
        hasil = []
        for tugas in self.daftar_tugas:
            data_dict = tugas.ke_dict()
            cocok = True

            for nama_atribut, nilai_target in kriteria.items():
                if nama_atribut not in data_dict:
                    cocok = False
                    break

                # Konversi string ke int/float jika diperlukan agar cocok
                nilai_aktual = data_dict[nama_atribut]
                if isinstance(nilai_aktual, str) and isinstance(nilai_target, str):
                    if nilai_aktual.lower() != nilai_target.lower():
                        cocok = False
                        break
                else:
                    if nilai_aktual != nilai_target:
                        cocok = False
                        break

            if cocok:
                hasil.append(tugas)

        return hasil


# ------------------------------------------------------------------ #
#  Uji Mandiri (Self-testing) Modul services.py
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    print("=== Uji Mandiri services.py ===")
    service = TugasService()
    print(f"Total tugas terdaftar: {len(service.ambil_semua())}")

    # Uji Pencarian
    hasil_cari = service.cari_tugas("Basis Data")
    print(f"Hasil cari 'Basis Data': {len(hasil_cari)} tugas")

    # Uji *args (Hitung jam)
    total_jam_semua = service.hitung_total_jam()
    print(f"Total jam seluruh tugas (*args default): {total_jam_semua:.1f} jam")

    # Uji **kwargs (Filter status)
    tugas_belum = service.filter_tugas(status="Belum", prioritas=1)
    print(f"Tugas Belum Selesai & Prioritas 1 (**kwargs): {len(tugas_belum)} tugas")

    # Uji Lambda (Pengurutan)
    terurut_deadline = service.urutkan_tugas(kunci="deadline")
    print(f"Deadline paling dekat: {terurut_deadline[0].deadline} ({terurut_deadline[0].judul})")
