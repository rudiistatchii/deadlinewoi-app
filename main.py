"""
main.py — Titik masuk utama (Entry Point) aplikasi DeadlineWoi.

Modul ini mengorkestrasi komponen-komponen aplikasi secara modular:
- Menggunakan TugasService sebagai pusat logika bisnis.
- Menyediakan menu interaktif di Terminal (CLI) yang ramah pengguna.
- Menyediakan opsi untuk meluncurkan Antarmuka Grafis Desktop (Tkinter GUI).

Cara menjalankan:
  python main.py         -> Membuka antarmuka Terminal (CLI)
  python main.py --gui   -> Langsung membuka antarmuka Grafis (Tkinter GUI)
"""

import sys
from services import TugasService


def cetak_tabel(daftar_tugas: list) -> None:
    """
    Menampilkan data tugas dalam format tabel rapi di terminal.

    Parameter
    ---------
    daftar_tugas : List objek Tugas yang akan ditampilkan.
    """
    if not daftar_tugas:
        print("\n[INFO] Tidak ada data tugas yang sesuai.")
        return

    garis = "=" * 96
    print("\n" + garis)
    print(f"{'ID':<6} {'JUDUL TUGAS':<30} {'MATA KULIAH':<24} {'DEADLINE':<12} {'JAM':<6} {'PRIO':<6} {'STATUS'}")
    print(garis)

    for t in daftar_tugas:
        judul = (t.judul[:27] + "..") if len(t.judul) > 29 else t.judul
        mk = (t.mata_kuliah[:21] + "..") if len(t.mata_kuliah) > 23 else t.mata_kuliah
        print(f"{t.id:<6} {judul:<30} {mk:<24} {t.deadline:<12} {t.bobot_jam:<6.1f} {t.prioritas:<6} {t.status}")

    print(garis)
    print(f"Total: {len(daftar_tugas)} tugas\n")


def menu_tampilkan_semua(service: TugasService) -> None:
    """Menu 1: Menampilkan seluruh data tugas."""
    print("\n--- DAFTAR SELURUH TUGAS KULIAH ---")
    semua = service.ambil_semua()
    cetak_tabel(semua)


def menu_cari_tugas(service: TugasService) -> None:
    """Menu 2: Mencari tugas berdasarkan kata kunci."""
    print("\n--- FITUR PENCARIAN TUGAS (SEARCHING) ---")
    kunci = input("Masukkan kata kunci (judul/mata kuliah/kategori/ID): ").strip()
    if not kunci:
        print("[!] Kata kunci tidak boleh kosong.")
        return

    hasil = service.cari_tugas(kunci)
    print(f"\nHasil pencarian untuk '{kunci}':")
    cetak_tabel(hasil)


def menu_urutkan_tugas(service: TugasService) -> None:
    """Menu 3: Mengurutkan data tugas menggunakan lambda."""
    print("\n--- FITUR PENGURUTAN TUGAS (SORTING DENGAN LAMBDA) ---")
    print("1. Deadline Terdekat (Ascending)")
    print("2. Prioritas Tertinggi (1 duluan)")
    print("3. Estimasi Jam Terbanyak (Descending)")
    print("4. Judul Tugas (A-Z)")

    pilihan = input("Pilih kriteria pengurutan (1-4): ").strip()
    if pilihan == "1":
        hasil = service.urutkan_tugas(kunci="deadline", menurun=False)
    elif pilihan == "2":
        hasil = service.urutkan_tugas(kunci="prioritas", menurun=False)
    elif pilihan == "3":
        hasil = service.urutkan_tugas(kunci="bobot_jam", menurun=True)
    elif pilihan == "4":
        hasil = service.urutkan_tugas(kunci="judul", menurun=False)
    else:
        print("[!] Pilihan tidak valid.")
        return

    cetak_tabel(hasil)


def menu_filter_tugas(service: TugasService) -> None:
    """Menu 4: Menyaring data tugas menggunakan **kwargs."""
    print("\n--- FITUR FILTER TUGAS (MENGGUNAKAN **KWARGS) ---")
    print("Filter berdasarkan Status:")
    print("1. Belum Selesai")
    print("2. Sedang Dalam Proses")
    print("3. Sudah Selesai")

    pilihan = input("Pilih filter status (1-3): ").strip()
    peta_status = {"1": "Belum", "2": "Proses", "3": "Selesai"}

    if pilihan in peta_status:
        # Memanggil filter_tugas dengan keyword argument status=...
        status_target = peta_status[pilihan]
        hasil = service.filter_tugas(status=status_target)
        print(f"\nTugas dengan status '{status_target}':")
        cetak_tabel(hasil)
    else:
        print("[!] Pilihan tidak valid.")


def menu_statistik_jam(service: TugasService) -> None:
    """Menu 5: Menghitung statistik jam menggunakan *args."""
    print("\n--- STATISTIK & AGREGASI WAKTU (MENGGUNAKAN *ARGS) ---")
    semua = service.ambil_semua()
    tugas_belum = service.filter_tugas(status="Belum")
    tugas_proses = service.filter_tugas(status="Proses")
    tugas_selesai = service.filter_tugas(status="Selesai")

    # Menggunakan *args untuk menghitung jam dari kumpulan tugas terpilih
    jam_total = service.hitung_total_jam()
    jam_belum = service.hitung_total_jam(*tugas_belum)
    jam_proses = service.hitung_total_jam(*tugas_proses)
    jam_selesai = service.hitung_total_jam(*tugas_selesai)

    print(f"Total Tugas Terdaftar : {len(semua)} tugas ({jam_total:.1f} jam)")
    print(f"  - Status Belum      : {len(tugas_belum)} tugas ({jam_belum:.1f} jam pengerjaan)")
    print(f"  - Status Proses     : {len(tugas_proses)} tugas ({jam_proses:.1f} jam pengerjaan)")
    print(f"  - Status Selesai    : {len(tugas_selesai)} tugas ({jam_selesai:.1f} jam pengerjaan)")


def menu_tambah_tugas(service: TugasService) -> None:
    """Menu 6: Menambahkan data tugas baru melalui terminal."""
    print("\n--- TAMBAH TUGAS KULIAH BARU ---")
    judul = input("Judul Tugas              : ").strip()
    matkul = input("Nama Mata Kuliah         : ").strip()
    print("Pilihan Kategori: Kuis, Tugas, Proyek, UTS, UAS")
    kategori = input("Kategori                 : ").strip()
    deadline = input("Deadline (YYYY-MM-DD)    : ").strip()
    bobot = input("Estimasi Jam (angka >= 0): ").strip()
    prioritas = input("Prioritas (1-3)          : ").strip()
    print("Pilihan Status: Belum, Proses, Selesai")
    status = input("Status                   : ").strip()

    data_input = {
        "id": "",
        "judul": judul,
        "mata_kuliah": matkul,
        "kategori": kategori,
        "deadline": deadline,
        "bobot_jam": bobot,
        "prioritas": prioritas,
        "status": status,
    }

    try:
        tugas_baru = service.tambah_tugas(data_input)
        print(f"\n[SUKSES] Tugas '{tugas_baru.judul}' berhasil ditambahkan dengan ID {tugas_baru.id}!")
    except ValueError as e:
        print(f"\n[GAGAL VALIDASI] {e}")


def jalankan_menu_cli() -> None:
    """Menjalankan loop menu utama CLI."""
    service = TugasService()

    while True:
        print("\n==============================================")
        print("     DEADLINEWOI - MANAJEMEN TUGAS KULIAH     ")
        print("==============================================")
        print("1. Tampilkan Semua Tugas")
        print("2. Cari Tugas (Searching)")
        print("3. Urutkan Tugas (Sorting dengan Lambda)")
        print("4. Filter Tugas Berdasarkan Status (**kwargs)")
        print("5. Statistik & Total Jam Pengerjaan (*args)")
        print("6. Tambah Tugas Baru")
        print("7. Buka Antarmuka Grafis Desktop (Tkinter GUI)")
        print("0. Keluar")
        print("----------------------------------------------")

        pilihan = input("Pilih menu (0-7): ").strip()

        if pilihan == "1":
            menu_tampilkan_semua(service)
        elif pilihan == "2":
            menu_cari_tugas(service)
        elif pilihan == "3":
            menu_urutkan_tugas(service)
        elif pilihan == "4":
            menu_filter_tugas(service)
        elif pilihan == "5":
            menu_statistik_jam(service)
        elif pilihan == "6":
            menu_tambah_tugas(service)
        elif pilihan == "7":
            print("\n[INFO] Meluncurkan Antarmuka Desktop Tkinter...")
            try:
                from ui import jalankan_ui
                jalankan_ui()
            except Exception as e:
                print(f"[!] Gagal membuka GUI: {e}")
        elif pilihan == "0":
            print("\nTerima kasih telah menggunakan DeadlineWoi. Semangat belajarnya!")
            break
        else:
            print("[!] Pilihan tidak valid. Silakan masukkan angka 0 sampai 7.")


if __name__ == "__main__":
    # Jika dijalankan dengan argumen --gui, langsung buka antarmuka grafis
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("--gui", "-g"):
        from ui import jalankan_ui
        jalankan_ui()
    else:
        jalankan_menu_cli()
