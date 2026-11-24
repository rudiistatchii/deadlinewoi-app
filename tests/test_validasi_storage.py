"""Pengujian unit untuk modul validasi dan penanganan file storage."""

import os  # mengelola dan menghapus file sementara
import tempfile  # membuat file CSV sementara untuk pengujian
import unittest  # framework pengujian unit otomatis

from validasi import validasi_bobot_jam, validasi_prioritas
from storage import muat_data


class TestValidasiDanStorage(unittest.TestCase):
    """Pengujian fungsi validasi batas input dan ketahanan baca CSV."""

    def test_validasi_bobot_jam_negatif(self) -> None:
        """Memastikan validasi_bobot_jam menolak nilai negatif."""
        with self.assertRaises(ValueError):
            validasi_bobot_jam(-1)

        with self.assertRaises(ValueError):
            validasi_bobot_jam("-5.5")

        # Memastikan nilai valid tetap diterima
        self.assertEqual(validasi_bobot_jam(2.5), 2.5)
        self.assertEqual(validasi_bobot_jam(0), 0.0)

    def test_validasi_prioritas_di_luar_rentang(self) -> None:
        """Memastikan validasi_prioritas menolak nilai di luar rentang 1-3."""
        with self.assertRaises(ValueError):
            validasi_prioritas(0)

        with self.assertRaises(ValueError):
            validasi_prioritas(4)

        with self.assertRaises(ValueError):
            validasi_prioritas("-1")

        with self.assertRaises(ValueError):
            validasi_prioritas("bukan_angka")

        # Memastikan nilai valid 1, 2, 3 diterima
        self.assertEqual(validasi_prioritas("1"), 1)
        self.assertEqual(validasi_prioritas(2), 2)
        self.assertEqual(validasi_prioritas(3), 3)

    def test_muat_data_csv_rusak(self) -> None:
        """Memastikan muat_data tidak crash saat membaca CSV dengan baris rusak."""
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        )
        # Menyiapkan 1 baris valid dan 3 baris dengan berbagai jenis kerusakan
        baris_csv = (
            "id,judul,mata_kuliah,kategori,deadline,bobot_jam,prioritas,status\n"
            "T001,Tugas Valid,Basis Data,Tugas,2026-11-20,3.0,1,Belum\n"
            "T002,Baris Kurang Kolom,Basis Data\n"
            "T003,Tanggal Tidak Valid,Basis Data,Tugas,2026-13-45,2.0,1,Belum\n"
            "T004,Bobot Jam Negatif,Basis Data,Tugas,2026-11-20,-5.0,1,Belum\n"
        )
        temp_file.write(baris_csv)
        temp_file.close()

        try:
            # Pembacaan tidak boleh crash dan hanya mengambil 1 baris yang valid
            hasil = muat_data(temp_file.name)
            self.assertEqual(len(hasil), 1)
            self.assertEqual(hasil[0].id, "T001")
            self.assertEqual(hasil[0].judul, "Tugas Valid")
        finally:
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)

    def test_muat_data_id_kosong_dan_duplikat(self) -> None:
        """Memastikan muat_data melewati baris dengan ID kosong atau ID duplikat."""
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        )
        baris_csv = (
            "id,judul,mata_kuliah,kategori,deadline,bobot_jam,prioritas,status\n"
            "T001,Tugas Valid Pertama,Basis Data,Tugas,2026-11-20,3.0,1,Belum\n"
            ",Tugas Tanpa ID,Struktur Data,Kuis,2026-11-22,2.0,2,Belum\n"
            "   ,Tugas ID Spasi,Jaringan Komputer,Tugas,2026-11-23,1.5,1,Belum\n"
            "T001,Tugas ID Duplikat,Analisis SI,Proyek,2026-12-01,5.0,3,Proses\n"
            "T002,Tugas Valid Kedua,Etika Profesi,Tugas,2026-11-25,2.0,2,Belum\n"
        )
        temp_file.write(baris_csv)
        temp_file.close()

        try:
            hasil = muat_data(temp_file.name)
            self.assertEqual(len(hasil), 2)
            self.assertEqual(hasil[0].id, "T001")
            self.assertEqual(hasil[0].judul, "Tugas Valid Pertama")
            self.assertEqual(hasil[1].id, "T002")
            self.assertEqual(hasil[1].judul, "Tugas Valid Kedua")
        finally:
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)


if __name__ == "__main__":
    unittest.main()
