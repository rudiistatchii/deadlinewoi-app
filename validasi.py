"""Menyediakan validasi untuk data tugas."""

from datetime import datetime  # memvalidasi format dan keabsahan tanggal

KATEGORI_VALID = {"Kuis", "Tugas", "Proyek", "UTS", "UAS"}
STATUS_VALID = {"Belum", "Proses", "Selesai"}
PRIORITAS_MIN = 1
PRIORITAS_MAX = 3
FORMAT_TANGGAL = "%Y-%m-%d"


def validasi_judul(judul: str) -> str:
    """Memastikan judul tugas tidak kosong."""
    judul_bersih = judul.strip()

    if not judul_bersih:
        raise ValueError("Judul tugas tidak boleh kosong.")

    return judul_bersih


def validasi_mata_kuliah(mata_kuliah: str) -> str:
    """Memastikan nama mata kuliah tidak kosong."""
    mk_bersih = mata_kuliah.strip()

    if not mk_bersih:
        raise ValueError("Nama mata kuliah tidak boleh kosong.")

    return mk_bersih


def validasi_kategori(kategori: str) -> str:
    """Memastikan kategori tugas termasuk dalam daftar yang diizinkan."""
    kategori_bersih = kategori.strip()

    if kategori_bersih not in KATEGORI_VALID:
        raise ValueError(
            f"Kategori '{kategori_bersih}' tidak valid. "
            f"Pilihan: {', '.join(sorted(KATEGORI_VALID))}."
        )

    return kategori_bersih


def validasi_deadline(deadline: str) -> str:
    """Memastikan deadline memakai format tanggal YYYY-MM-DD yang valid."""
    deadline_bersih = deadline.strip()

    try:
        datetime.strptime(deadline_bersih, FORMAT_TANGGAL)
    except ValueError:
        raise ValueError(
            f"Deadline '{deadline_bersih}' tidak valid. "
            f"Gunakan format YYYY-MM-DD, contoh: 2026-12-31."
        )

    return deadline_bersih


def validasi_bobot_jam(bobot_jam) -> float:
    """Memastikan bobot jam berupa angka non-negatif."""
    try:
        nilai = float(bobot_jam)
    except (ValueError, TypeError):
        raise ValueError(
            f"Bobot jam '{bobot_jam}' harus berupa angka, contoh: 3 atau 1.5."
        )

    if nilai < 0:
        raise ValueError(
            f"Bobot jam tidak boleh negatif. Nilai yang diberikan: {nilai}."
        )

    assert nilai >= 0, "Validasi internal gagal: bobot jam harus non-negatif."

    return nilai


def validasi_prioritas(prioritas) -> int:
    """Memastikan prioritas berupa bilangan bulat dalam rentang yang diizinkan."""
    try:
        nilai = int(prioritas)
    except (ValueError, TypeError):
        raise ValueError(
            f"Prioritas '{prioritas}' harus berupa bilangan bulat."
        )

    if not (PRIORITAS_MIN <= nilai <= PRIORITAS_MAX):
        raise ValueError(
            f"Prioritas harus antara {PRIORITAS_MIN} dan {PRIORITAS_MAX}. "
            f"Nilai yang diberikan: {nilai}."
        )

    return nilai


def validasi_status(status: str) -> str:
    """Memastikan status tugas termasuk dalam daftar yang diizinkan."""
    status_bersih = status.strip()

    if status_bersih not in STATUS_VALID:
        raise ValueError(
            f"Status '{status_bersih}' tidak valid. "
            f"Pilihan: {', '.join(sorted(STATUS_VALID))}."
        )

    return status_bersih


def validasi_semua(data: dict) -> dict:
    """Memvalidasi dan membersihkan seluruh field data tugas."""
    return {
        "id": data["id"].strip(),
        "judul": validasi_judul(data["judul"]),
        "mata_kuliah": validasi_mata_kuliah(data["mata_kuliah"]),
        "kategori": validasi_kategori(data["kategori"]),
        "deadline": validasi_deadline(data["deadline"]),
        "bobot_jam": validasi_bobot_jam(data["bobot_jam"]),
        "prioritas": validasi_prioritas(data["prioritas"]),
        "status": validasi_status(data["status"]),
    }


