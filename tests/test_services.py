"""
test_services.py — Modul pengujian otomatis menggunakan unittest.

Memenuhi ketentuan penilaian UAS:
- Menggunakan framework standar unittest
- Memiliki minimal 1 Class Pengujian (TestTugasService)
- Memiliki minimal 4-5 fungsi pengujian (test cases) untuk menguji pengolahan data,
  pencarian, dan pengurutan secara terisolasi tanpa antarmuka grafis (UI).
"""

import os
import tempfile
import unittest

from models import Tugas
from services import TugasService


class TestTugasService(unittest.TestCase):
    """
    Kelas pengujian unit untuk logika bisnis pada class TugasService.
    """

    def setUp(self) -> None:
        """
        Dijalankan sebelum setiap method tes.
        Membuat file CSV sementara (dummy) agar pengujian tidak mengotori
        file database data/tugas.csv yang asli.
        """
        # Buat file CSV temporer
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        )
        # Isi data awal pengujian
        header = "id,judul,mata_kuliah,kategori,deadline,bobot_jam,prioritas,status\n"
        baris1 = "T001,Tugas Basis Data,Basis Data,Tugas,2026-11-20,4.0,1,Belum\n"
        baris2 = "T002,Kuis Struktur Data,Struktur Data,Kuis,2026-11-15,2.0,2,Proses\n"
        baris3 = "T003,Proyek SI,Analisis SI,Proyek,2026-12-05,10.0,1,Selesai\n"

        self.temp_file.write(header + baris1 + baris2 + baris3)
        self.temp_file.close()

        # Inisialisasi service menggunakan file CSV sementara tersebut
        self.service = TugasService(path_csv=self.temp_file.name)

    def tearDown(self) -> None:
        """
        Dijalankan setelah setiap method tes selesai.
        Menghapus file CSV sementara untuk menjaga kebersihan sistem.
        """
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    # ------------------------------------------------------------------ #
    #  Test Case 1: Pengambilan dan Penambahan Tugas Baru
    # ------------------------------------------------------------------ #

    def test_ambil_dan_tambah_tugas(self) -> None:
        """Menguji apakah data awal terbaca dan tugas baru bisa ditambahkan."""
        # Awalnya ada 3 tugas di file sementara
        self.assertEqual(len(self.service.ambil_semua()), 3)

        # Tambahkan tugas baru
        input_baru = {
            "judul": "Uji Unit Testing",
            "mata_kuliah": "Pemrograman Terstruktur",
            "kategori": "Tugas",
            "deadline": "2026-12-10",
            "bobot_jam": "3.5",
            "prioritas": "1",
            "status": "Belum",
        }
        tugas_dibuat = self.service.tambah_tugas(input_baru)

        # Pastikan tugas berhasil masuk dan ID otomatis terbuat
        self.assertEqual(len(self.service.ambil_semua()), 4)
        self.assertEqual(tugas_dibuat.id, "T004")
        self.assertEqual(tugas_dibuat.judul, "Uji Unit Testing")

    # ------------------------------------------------------------------ #
    #  Test Case 2: Algoritma Pencarian Kata Kunci (Searching)
    # ------------------------------------------------------------------ #

    def test_cari_tugas(self) -> None:
        """Menguji fitur pencarian kata kunci pada judul atau mata kuliah."""
        # Cari kata kunci 'Basis Data'
        hasil_bd = self.service.cari_tugas("Basis Data")
        self.assertEqual(len(hasil_bd), 1)
        self.assertEqual(hasil_bd[0].id, "T001")

        # Cari kata kunci case-insensitive 'kuis'
        hasil_kuis = self.service.cari_tugas("kuis")
        self.assertEqual(len(hasil_kuis), 1)
        self.assertEqual(hasil_kuis[0].kategori, "Kuis")

        # Cari kata kunci yang tidak ada
        hasil_nihil = self.service.cari_tugas("Akuntansi")
        self.assertEqual(len(hasil_nihil), 0)

    # ------------------------------------------------------------------ #
    #  Test Case 3: Algoritma Pengurutan Menggunakan Lambda (Sorting)
    # ------------------------------------------------------------------ #

    def test_urutkan_tugas_lambda(self) -> None:
        """Menguji pengurutan data berdasarkan deadline dan bobot jam."""
        # Urutkan berdasarkan deadline (Ascending: tanggal paling awal duluan)
        terurut_deadline = self.service.urutkan_tugas(kunci="deadline", menurun=False)
        self.assertEqual(terurut_deadline[0].id, "T002")  # 2026-11-15
        self.assertEqual(terurut_deadline[-1].id, "T003") # 2026-12-05

        # Urutkan berdasarkan bobot jam (Descending: jam terbesar duluan)
        terurut_bobot = self.service.urutkan_tugas(kunci="bobot_jam", menurun=True)
        self.assertEqual(terurut_bobot[0].id, "T003")  # 10.0 jam
        self.assertEqual(terurut_bobot[-1].id, "T002") # 2.0 jam

    # ------------------------------------------------------------------ #
    #  Test Case 4: Penggunaan *args pada Perhitungan Agregasi Jam
    # ------------------------------------------------------------------ #

    def test_hitung_total_jam_args(self) -> None:
        """Menguji fungsi hitung_total_jam dengan memanfaatkan konsep *args."""
        # 1. Tanpa argumen (menghitung seluruh tugas: 4.0 + 2.0 + 10.0 = 16.0)
        total_semua = self.service.hitung_total_jam()
        self.assertEqual(total_semua, 16.0)

        # 2. Mengirim beberapa objek tugas pilihan sebagai *args
        t1 = self.service.ambil_berdasarkan_id("T001")
        t2 = self.service.ambil_berdasarkan_id("T002")
        self.assertIsNotNone(t1)
        self.assertIsNotNone(t2)

        total_dua_tugas = self.service.hitung_total_jam(t1, t2)
        self.assertEqual(total_dua_tugas, 6.0)

    # ------------------------------------------------------------------ #
    #  Test Case 5: Penggunaan **kwargs pada Penyaringan Data (Filtering)
    # ------------------------------------------------------------------ #

    def test_filter_tugas_kwargs(self) -> None:
        """Menguji fungsi filter_tugas dengan memanfaatkan konsep **kwargs."""
        # Filter berdasarkan status
        tugas_selesai = self.service.filter_tugas(status="Selesai")
        self.assertEqual(len(tugas_selesai), 1)
        self.assertEqual(tugas_selesai[0].id, "T003")

        # Filter berdasarkan kombinasi prioritas dan kategori
        tugas_prioritas_1 = self.service.filter_tugas(prioritas=1, kategori="Tugas")
        self.assertEqual(len(tugas_prioritas_1), 1)
        self.assertEqual(tugas_prioritas_1[0].id, "T001")

    # ------------------------------------------------------------------ #
    #  Test Case 6: Pembaruan Status & Penanganan Error Validasi
    # ------------------------------------------------------------------ #

    def test_perbarui_status_dan_validasi(self) -> None:
        """Menguji perbaruan status dan penolakan jika status tidak valid."""
        # Update berhasil
        tugas_update = self.service.perbarui_status("T001", "Selesai")
        self.assertEqual(tugas_update.status, "Selesai")

        # Status salah harus melempar ValueError
        with self.assertRaises(ValueError):
            self.service.perbarui_status("T001", "Batal")


if __name__ == "__main__":
    unittest.main()
