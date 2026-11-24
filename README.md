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
│   ├── __init__.py               # Package marker
│   ├── test_algoritma.py         # Unit test algoritma merge sort (5 test cases)
│   ├── test_services.py          # Unit test logika bisnis (6 test cases)
│   └── test_validasi_storage.py  # Unit test validasi & file handling (4 test cases)
├── .gitignore           # File pengabaian git (mengabaikan __pycache__/)
├── algoritma.py         # Layer Algoritma: Pengurutan Merge Sort rekursif dan stabil
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
| **Unit Testing** | 3 kelas pengujian dengan total 15 fungsi uji independen dari UI. | `tests/` |
| **Antarmuka Pengguna (UI)** | GUI desktop Tkinter berbasis tabular (`ttk.Treeview`), form input, dan tombol aksi. | `ui.py` |

---

## 3. Cara Menjalankan Aplikasi

Jalankan perintah berikut di terminal:

### A. Menjalankan Antarmuka Grafis Desktop (Tkinter GUI) — Default
```bash
# Langsung membuka GUI desktop
python main.py

# Atau bisa juga menjalankan modul UI secara langsung
python ui.py
```

### B. Menjalankan Antarmuka Terminal (CLI)
```bash
# Menjalankan menu interaktif di terminal dengan opsi --cli
python main.py --cli
```
Menyediakan menu interaktif di terminal untuk melihat tabel, mencari, mengurutkan, menyaring tugas, melihat statistik jam, serta menambah tugas baru.

### C. Menjalankan Pengujian Unit Otomatis (Unit Testing)
```bash
python -m unittest discover tests
```
Semua 15 test case akan diuji secara otomatis dan mandiri menggunakan file CSV sementara tanpa mengotori data asli.
