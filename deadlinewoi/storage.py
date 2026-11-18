
import csv
import os

from models import Tugas
from validasi import validasi_semua


HEADER_CSV = Tugas.HEADER


def muat_data(path: str) -> list:
    """Memuat tugas dari file CSV."""
    daftar_tugas = []

    try:
        with open(path, mode="r", encoding="utf-8", newline="") as file_csv:
            pembaca = csv.DictReader(file_csv)

            for nomor_baris, baris in enumerate(pembaca, start=2):
                try:
                    data_valid = validasi_semua(baris)
                    tugas = Tugas.dari_dict(data_valid)
                    daftar_tugas.append(tugas)

                except ValueError as e:
                    print(f"[PERINGATAN] Baris {nomor_baris} dilewati — {e}")

    except FileNotFoundError:
        print(f"[INFO] File '{path}' tidak ditemukan. Membuat file baru...")
        _buat_file_baru(path)

    return daftar_tugas


def simpan_data(path: str, daftar_tugas: list) -> None:
    """Menyimpan seluruh daftar tugas ke file CSV."""
    _pastikan_folder_ada(path)

    with open(path, mode="w", encoding="utf-8", newline="") as file_csv:
        penulis = csv.DictWriter(file_csv, fieldnames=HEADER_CSV)
        penulis.writeheader()

        for tugas in daftar_tugas:
            penulis.writerow(tugas.ke_dict())

    print(f"[INFO] Data berhasil disimpan ke '{path}' ({len(daftar_tugas)} tugas).")


def tambah_baris(path: str, tugas: Tugas) -> None:
    """Menambahkan satu tugas ke akhir file CSV."""
    file_baru = not os.path.exists(path)
    _pastikan_folder_ada(path)

    with open(path, mode="a", encoding="utf-8", newline="") as file_csv:
        penulis = csv.DictWriter(file_csv, fieldnames=HEADER_CSV)

        if file_baru:
            penulis.writeheader()

        penulis.writerow(tugas.ke_dict())

    print(f"[INFO] Tugas '{tugas.judul}' berhasil ditambahkan ke '{path}'.")


def _buat_file_baru(path: str) -> None:
    """Membuat file CSV baru dengan baris header."""
    _pastikan_folder_ada(path)

    with open(path, mode="w", encoding="utf-8", newline="") as file_csv:
        penulis = csv.DictWriter(file_csv, fieldnames=HEADER_CSV)
        penulis.writeheader()

    print(f"[INFO] File baru '{path}' berhasil dibuat dengan header.")


def _pastikan_folder_ada(path: str) -> None:
    """Membuat folder induk jika belum tersedia."""
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
        print(f"[INFO] Folder '{folder}' berhasil dibuat.")
