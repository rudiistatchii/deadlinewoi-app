import os
import tempfile
import unittest

from services import TugasService


class TestTugasService(unittest.TestCase):
    """Pengujian unit logika bisnis TugasService."""

    def setUp(self) -> None:
        """Inisialisasi file CSV sementara sebelum pengujian."""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        )
        header = "id,judul,mata_kuliah,kategori,deadline,bobot_jam,prioritas,status\n"
        baris1 = "T001,Tugas Basis Data,Basis Data,Tugas,2026-11-20,4.0,1,Belum\n"
        baris2 = "T002,Kuis Struktur Data,Struktur Data,Kuis,2026-11-15,2.0,2,Proses\n"
        baris3 = "T003,Proyek SI,Analisis SI,Proyek,2026-12-05,10.0,1,Selesai\n"

        self.temp_file.write(header + baris1 + baris2 + baris3)
        self.temp_file.close()

        self.service = TugasService(path_csv=self.temp_file.name)

    def tearDown(self) -> None:
        """Hapus file CSV sementara setelah pengujian."""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_ambil_dan_tambah_tugas(self) -> None:
        """Uji pembacaan awal dan penambahan tugas baru."""
        self.assertEqual(len(self.service.ambil_semua()), 3)

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

        self.assertEqual(len(self.service.ambil_semua()), 4)
        self.assertEqual(tugas_dibuat.id, "T004")
        self.assertEqual(tugas_dibuat.judul, "Uji Unit Testing")

    def test_cari_tugas(self) -> None:
        """Uji pencarian kata kunci pada tugas."""
        hasil_bd = self.service.cari_tugas("Basis Data")
        self.assertEqual(len(hasil_bd), 1)
        self.assertEqual(hasil_bd[0].id, "T001")

        hasil_kuis = self.service.cari_tugas("kuis")
        self.assertEqual(len(hasil_kuis), 1)
        self.assertEqual(hasil_kuis[0].kategori, "Kuis")

        hasil_nihil = self.service.cari_tugas("Akuntansi")
        self.assertEqual(len(hasil_nihil), 0)

    def test_urutkan_tugas_lambda(self) -> None:
        """Uji pengurutan tugas menggunakan lambda."""
        terurut_deadline = self.service.urutkan_tugas(kunci="deadline", menurun=False)
        self.assertEqual(terurut_deadline[0].id, "T002")
        self.assertEqual(terurut_deadline[-1].id, "T003")

        terurut_bobot = self.service.urutkan_tugas(kunci="bobot_jam", menurun=True)
        self.assertEqual(terurut_bobot[0].id, "T003")
        self.assertEqual(terurut_bobot[-1].id, "T002")

    def test_hitung_total_jam_args(self) -> None:
        """Uji agregasi total jam menggunakan *args."""
        total_semua = self.service.hitung_total_jam()
        self.assertEqual(total_semua, 16.0)

        t1 = self.service.ambil_berdasarkan_id("T001")
        t2 = self.service.ambil_berdasarkan_id("T002")
        self.assertIsNotNone(t1)
        self.assertIsNotNone(t2)

        total_dua_tugas = self.service.hitung_total_jam(t1, t2)
        self.assertEqual(total_dua_tugas, 6.0)

    def test_filter_tugas_kwargs(self) -> None:
        """Uji filter tugas menggunakan **kwargs."""
        tugas_selesai = self.service.filter_tugas(status="Selesai")
        self.assertEqual(len(tugas_selesai), 1)
        self.assertEqual(tugas_selesai[0].id, "T003")

        tugas_prioritas_1 = self.service.filter_tugas(prioritas=1, kategori="Tugas")
        self.assertEqual(len(tugas_prioritas_1), 1)
        self.assertEqual(tugas_prioritas_1[0].id, "T001")

    def test_perbarui_status_dan_validasi(self) -> None:
        """Uji ubah status dan validasi input salah."""
        tugas_update = self.service.perbarui_status("T001", "Selesai")
        self.assertEqual(tugas_update.status, "Selesai")

        with self.assertRaises(ValueError):
            self.service.perbarui_status("T001", "Batal")


if __name__ == "__main__":
    unittest.main()
