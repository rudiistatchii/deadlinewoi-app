import os  # mengelola jalur direktori dan menghapus file sementara
import tempfile  # membuat file CSV tiruan sementara untuk pengujian
import unittest  # framework pengujian unit otomatis

from algoritma import merge_sort
from services import TugasService


class TestMergeSort(unittest.TestCase):
    """Pengujian unit algoritma Merge Sort dan komparasi dengan pengurutan bawaan."""

    def setUp(self) -> None:
        """Inisialisasi file CSV sementara sebelum pengujian."""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", encoding="utf-8"
        )
        header = "id,judul,mata_kuliah,kategori,deadline,bobot_jam,prioritas,status\n"
        baris1 = "T001,Tugas Basis Data,Basis Data,Tugas,2026-11-20,4.0,1,Belum\n"
        baris2 = "T002,Kuis Struktur Data,Struktur Data,Kuis,2026-11-15,2.0,2,Proses\n"
        baris3 = "T003,Proyek SI,Analisis SI,Proyek,2026-12-05,10.0,1,Selesai\n"
        baris4 = "T004,Makalah Etika,Etika Profesi,Tugas,2026-11-20,2.0,3,Belum\n"
        baris5 = "T005,Praktikum Jaringan,Jaringan Komputer,Tugas,2026-11-10,6.0,2,Proses\n"

        self.temp_file.write(header + baris1 + baris2 + baris3 + baris4 + baris5)
        self.temp_file.close()

        self.service = TugasService(path_csv=self.temp_file.name)

    def tearDown(self) -> None:
        """Hapus file CSV sementara setelah pengujian."""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_urutan_naik_angka_acak(self) -> None:
        """Uji urutan naik pada angka acak menghasilkan hasil yang benar."""
        angka_acak = [42, 17, 89, 5, 23, 1, 99, 12, 55, 34]
        hasil = merge_sort(angka_acak)
        ekspektasi = [1, 5, 12, 17, 23, 34, 42, 55, 89, 99]
        self.assertEqual(hasil, ekspektasi)

    def test_urutan_menurun(self) -> None:
        """Uji urutan menurun (terbalik=True) menghasilkan urutan dari terbesar ke terkecil."""
        angka_acak = [42, 17, 89, 5, 23, 1, 99, 12, 55, 34]
        hasil = merge_sort(angka_acak, terbalik=True)
        ekspektasi = [99, 89, 55, 42, 34, 23, 17, 12, 5, 1]
        self.assertEqual(hasil, ekspektasi)

    def test_stabilitas_pengurutan(self) -> None:
        """Uji stabilitas: dua elemen dengan kunci sama tetap dalam urutan semula (naik dan turun)."""
        data = [("A", 2), ("B", 1), ("C", 2), ("D", 1), ("E", 2)]

        # Uji urutan naik berdasarkan angka kedua
        hasil_naik = merge_sort(data, kunci=lambda x: x[1], terbalik=False)
        ekspektasi_naik = [("B", 1), ("D", 1), ("A", 2), ("C", 2), ("E", 2)]
        self.assertEqual(hasil_naik, ekspektasi_naik)

        # Uji urutan menurun berdasarkan angka kedua
        hasil_turun = merge_sort(data, kunci=lambda x: x[1], terbalik=True)
        ekspektasi_turun = [("A", 2), ("C", 2), ("E", 2), ("B", 1), ("D", 1)]
        self.assertEqual(hasil_turun, ekspektasi_turun)

    def test_list_kosong_satu_elemen_dan_immutability(self) -> None:
        """Uji list kosong dan 1 elemen tidak error, serta list asli tidak berubah."""
        # List kosong
        self.assertEqual(merge_sort([]), [])

        # List 1 elemen
        self.assertEqual(merge_sort([99]), [99])

        # List asli tidak termutasi (immutability)
        daftar_asli = [5, 2, 8, 1, 9]
        salinan_asli = list(daftar_asli)
        hasil = merge_sort(daftar_asli)

        self.assertEqual(daftar_asli, salinan_asli)
        self.assertIsNot(hasil, daftar_asli)

    def test_identik_dengan_urutkan_tugas_bawaan(self) -> None:
        """Uji hasil urutkan_tugas (merge sort) identik dengan urutkan_tugas_bawaan (sorted) untuk semua kriteria."""
        kriteria_list = ["deadline", "prioritas", "bobot_jam", "judul", "mata_kuliah"]

        for kriteria in kriteria_list:
            for menurun in [False, True]:
                hasil_merge = self.service.urutkan_tugas(kunci=kriteria, menurun=menurun)
                hasil_bawaan = self.service.urutkan_tugas_bawaan(kunci=kriteria, menurun=menurun)

                id_merge = [t.id for t in hasil_merge]
                id_bawaan = [t.id for t in hasil_bawaan]

                self.assertEqual(
                    id_merge,
                    id_bawaan,
                    f"Hasil berbeda pada kriteria '{kriteria}' dengan menurun={menurun}",
                )


if __name__ == "__main__":
    unittest.main()
