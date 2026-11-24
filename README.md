# DeadlineWoi — Sistem Manajemen Tugas Kuliah

> Aplikasi desktop manajemen tugas dan deadline kuliah berbasis Python dengan arsitektur **Pemrograman Modular**.  
> Proyek Ujian Akhir Semester (UAS) mata kuliah **Pemrograman Terstruktur** (Prodi S1 Sistem Informasi).

---

## 1. Konsep & Arsitektur Modular

Aplikasi ini memisahkan setiap tanggung jawab (*Separation of Concerns*) ke dalam modul-modul independen:

```
deadlinewoi/
├── data/
│   └── tugas.csv        # Database tabular berbasis CSV
├── tests/
│   ├── __init__.py      # Package marker
│   └── test_services.py # Unit test otomatis (unittest)
├── .gitignore           # File pengabaian git (mengabaikan __pycache__/)
├── main.py              # Entry Point: Menu terminal interaktif dan peluncur aplikasi
├── models.py            # Layer Data: Class Tugas (blueprint objek data)
├── README.md            # Dokumentasi lengkap proyek
├── services.py          # Layer Bisnis: Class TugasService (*args, **kwargs, lambda, CRUD)
├── storage.py           # Layer Penyimpanan: I/O file CSV dengan 'with open()' ('r', 'w', 'a')
├── ui.py                # Layer Presentasi: Antarmuka GUI Tkinter (Treeview, Form, Filter)
└── validasi.py          # Layer Validasi: Fungsi-fungsi pengecekan integritas input
```

### Hubungan Antar Modul:
```
[ UI (ui.py) / CLI (main.py) ]
             │
             ▼
[ Service Layer (services.py) ]
     ├──► [ Validasi (validasi.py) ]
     ├──► [ Model Objek (models.py) ]
     └──► [ File Storage (storage.py) ] ◄──► [ data/tugas.csv ]
```

---

## 2. Pemenuhan Kriteria Teknis Proyek (UAS)

| Aspek Penilaian | Implementasi di DeadlineWoi | Lokasi Modul |
| :--- | :--- | :--- |
| **Penerapan OOP** | Minimal 2 Class: `Tugas`, `TugasService`, dan `DeadlineWoiUI`. | `models.py`, `services.py`, `ui.py` |
| **Agregasi (*args)** | Method `hitung_total_jam(*tugas_pilihan)` menghitung jam pengerjaan kumpulan tugas. | `services.py` |
| **Filter Fleksibel (**kwargs)** | Method `filter_tugas(**kriteria)` menyaring data berdasarkan atribut apapun. | `services.py` |
| **Lambda & Sorting** | `urutkan_tugas(kunci=..., menurun=...)` menggunakan `sorted(..., key=lambda t: ...)`. | `services.py` |
| **Pencarian (Searching)** | Method `cari_tugas(kata_kunci)` dengan algoritma pencarian teks case-insensitive. | `services.py` |
| **File Handling Aman** | Seluruh baca/tulis memakai `with open()`, mendukung mode `'r'`, `'w'`, dan `'a'`. | `storage.py` |
| **Error Handling** | Penanganan `FileNotFoundError`, `ValueError`, `raise`, dan penggunaan `assert`. | `storage.py`, `validasi.py` |
| **Unit Testing** | Kelas pengujian `TestTugasService` dengan 6 fungsi uji independen dari UI. | `tests/test_services.py` |
| **Antarmuka Pengguna (UI)** | GUI desktop Tkinter berbasis tabular (`ttk.Treeview`), form input, dan tombol aksi. | `ui.py` |

---

## 3. Cara Menjalankan Aplikasi

Jalankan perintah berikut di terminal:

### A. Menjalankan Antarmuka Terminal (CLI)
```bash
python main.py
```
Menyediakan menu interaktif untuk melihat tabel, mencari, mengurutkan, menyaring tugas, melihat statistik jam, serta menambah tugas baru.

### B. Menjalankan Antarmuka Grafis Desktop (Tkinter GUI)
```bash
# Opsi 1: Menjalankan modul UI langsung
python ui.py

# Opsi 2: Menjalankan lewat main dengan argumen --gui
python main.py --gui
```

### C. Menjalankan Pengujian Unit Otomatis (Unit Testing)
```bash
python -m unittest discover tests
```
Semua 6 test case akan diuji secara otomatis dan mandiri menggunakan file CSV sementara tanpa mengotori data asli.

---

## 4. Pengujian Mandiri per Modul (*Smoke Testing*)

Setiap modul inti memiliki blok `if __name__ == "__main__":` sehingga dapat diuji sendiri-sendiri langsung dari terminal:
```bash
python models.py    # Uji coba pembuatan objek Tugas
python validasi.py  # Uji coba penolakan input tidak valid
python storage.py   # Uji coba pembacaan file CSV
python services.py  # Uji coba logika bisnis (cari, urut, filter, total jam)
```
