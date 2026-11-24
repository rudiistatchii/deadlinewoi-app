"""Modul algoritma pengurutan data untuk aplikasi DeadlineWoi."""

from typing import Any, Callable, List, Optional


def gabung(
    kiri: List[Any],
    kanan: List[Any],
    kunci: Optional[Callable[[Any], Any]] = None,
    terbalik: bool = False,
) -> List[Any]:
    """Menggabungkan dua sub-list terurut menjadi satu list terurut baru (stabil)."""
    hasil = []
    i = 0
    j = 0

    while i < len(kiri) and j < len(kanan):
        # Ambil nilai kunci pembanding jika parameter kunci diberikan
        nilai_kiri = kunci(kiri[i]) if kunci is not None else kiri[i]
        nilai_kanan = kunci(kanan[j]) if kunci is not None else kanan[j]

        # Pengecekan stabilitas:
        # - Urutan naik (terbalik=False): ambil elemen kiri jika nilai_kiri <= nilai_kanan
        # - Urutan turun (terbalik=True): ambil elemen kiri jika nilai_kiri >= nilai_kanan
        # Tanda sama dengan (=) menjamin elemen bernilai sama tetap pada urutan semula
        if (not terbalik and nilai_kiri <= nilai_kanan) or (terbalik and nilai_kiri >= nilai_kanan):
            hasil.append(kiri[i])
            i += 1
        else:
            hasil.append(kanan[j])
            j += 1

    # Masukkan sisa elemen yang belum terambil
    hasil.extend(kiri[i:])
    hasil.extend(kanan[j:])
    return hasil


def merge_sort(
    daftar: List[Any],
    kunci: Optional[Callable[[Any], Any]] = None,
    terbalik: bool = False,
) -> List[Any]:
    """
    Mengurutkan list menggunakan algoritma Merge Sort secara rekursif (stabil).

    Ide Algoritma (Divide and Conquer):
    1. Membagi list menjadi dua bagian berukuran hampir sama hingga ukuran 0 atau 1.
    2. Mengurutkan tiap bagian secara rekursif.
    3. Menggabungkan (merge) dua bagian terurut menjadi satu list baru.

    Kompleksitas Algoritma:
    - Waktu: O(n log n) pada kasus terbaik, rata-rata, dan terburuk.
    - Memori Tambahan: O(n) untuk alokasi list hasil penggabungan.
    """
    # Basis rekursi: list kosong atau 1 elemen sudah terurut, kembalikan salinan baru
    if len(daftar) <= 1:
        return list(daftar)

    # Bagi list menjadi dua bagian
    tengah = len(daftar) // 2
    kiri_terurut = merge_sort(daftar[:tengah], kunci=kunci, terbalik=terbalik)
    kanan_terurut = merge_sort(daftar[tengah:], kunci=kunci, terbalik=terbalik)

    # Gabungkan kedua bagian terurut
    return gabung(kiri_terurut, kanan_terurut, kunci=kunci, terbalik=terbalik)
