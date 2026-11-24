import os
from typing import List, Optional

from models import Tugas
import storage
import validasi


class TugasService:
    """Pengelola data dan logika bisnis tugas."""

    def __init__(self, path_csv: Optional[str] = None) -> None:
        """Inisialisasi service dan muat data tugas dari CSV."""
        if path_csv is None:
            folder_ini = os.path.dirname(os.path.abspath(__file__))
            self.path_csv = os.path.join(folder_ini, "data", "tugas.csv")
        else:
            self.path_csv = path_csv

        self.daftar_tugas: List[Tugas] = []
        self.muat()

    def muat(self) -> List[Tugas]:
        """Muat ulang seluruh tugas dari file CSV."""
        self.daftar_tugas = storage.muat_data(self.path_csv)
        return self.daftar_tugas

    def simpan(self) -> None:
        """Tulis seluruh data tugas ke file CSV."""
        storage.simpan_data(self.path_csv, self.daftar_tugas)

    def ambil_semua(self) -> List[Tugas]:
        """Ambil seluruh daftar tugas."""
        return list(self.daftar_tugas)

    def ambil_berdasarkan_id(self, id_tugas: str) -> Optional[Tugas]:
        """Cari tugas berdasarkan ID."""
        id_target = id_tugas.strip().upper()
        for tugas in self.daftar_tugas:
            if tugas.id.upper() == id_target:
                return tugas
        return None

    def buat_id_otomatis(self) -> str:
        """Generate ID baru secara berurutan (contoh: T022)."""
        angka_maks = 0
        for tugas in self.daftar_tugas:
            if tugas.id.startswith("T") and tugas.id[1:].isdigit():
                angka = int(tugas.id[1:])
                if angka > angka_maks:
                    angka_maks = angka
        return f"T{angka_maks + 1:03d}"

    def tambah_tugas(self, data_input: dict) -> Tugas:
        """Validasi dan tambahkan satu tugas baru."""
        if "id" not in data_input or not data_input["id"].strip():
            data_input["id"] = self.buat_id_otomatis()

        if self.ambil_berdasarkan_id(data_input["id"]) is not None:
            raise ValueError(f"Tugas dengan ID '{data_input['id']}' sudah ada.")

        data_valid = validasi.validasi_semua(data_input)
        tugas_baru = Tugas.dari_dict(data_valid)

        self.daftar_tugas.append(tugas_baru)
        storage.tambah_baris(self.path_csv, tugas_baru)
        return tugas_baru

    def hapus_tugas(self, id_tugas: str) -> bool:
        """Hapus tugas berdasarkan ID."""
        tugas = self.ambil_berdasarkan_id(id_tugas)
        if tugas is None:
            return False

        self.daftar_tugas.remove(tugas)
        self.simpan()
        return True

    def perbarui_status(self, id_tugas: str, status_baru: str) -> Tugas:
        """Perbarui status pengerjaan suatu tugas."""
        status_valid = validasi.validasi_status(status_baru)
        tugas = self.ambil_berdasarkan_id(id_tugas)

        if tugas is None:
            raise ValueError(f"Tugas dengan ID '{id_tugas}' tidak ditemukan.")

        tugas.status = status_valid
        self.simpan()
        return tugas

    def cari_tugas(self, kata_kunci: str, kolom: str = "semua") -> List[Tugas]:
        """Pencarian tugas berdasarkan kata kunci (Linear Search)."""
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
            else:
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
        """Pengurutan data tugas menggunakan lambda."""
        target = self.daftar_tugas if daftar is None else daftar

        peta_kunci = {
            "deadline": lambda t: t.deadline,
            "prioritas": lambda t: t.prioritas,
            "bobot_jam": lambda t: t.bobot_jam,
            "judul": lambda t: t.judul.lower(),
            "mata_kuliah": lambda t: t.mata_kuliah.lower(),
        }

        fungsi_kunci = peta_kunci.get(kunci, lambda t: t.deadline)
        return sorted(target, key=fungsi_kunci, reverse=menurun)

    def hitung_total_jam(self, *tugas_pilihan: Tugas) -> float:
        """Hitung total estimasi jam pengerjaan (*args)."""
        return sum(t.bobot_jam for t in tugas_pilihan)

    def hitung_total_semua(self) -> float:
        """Hitung total estimasi jam dari seluruh tugas yang ada."""
        return self.hitung_total_jam(*self.daftar_tugas)

    def filter_tugas(self, **kriteria) -> List[Tugas]:
        """Filter daftar tugas secara dinamis (**kwargs)."""
        hasil = []
        for tugas in self.daftar_tugas:
            data_dict = tugas.ke_dict()
            cocok = True

            for nama_atribut, nilai_target in kriteria.items():
                if nama_atribut not in data_dict:
                    cocok = False
                    break

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


if __name__ == "__main__":
    service = TugasService()
    print("Total tugas:", len(service.ambil_semua()))
    print("Total jam (*args):", service.hitung_total_semua())
