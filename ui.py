"""
ui.py — Modul antarmuka pengguna grafis (GUI) berbasis Tkinter untuk DeadlineWoi.

Modul ini mengimplementasikan lapisan presentasi (Presentation Layer) secara modular.
Sesuai prinsip pemrograman modular:
- UI HANYA bertugas menampilkan data dan menangkap interaksi pengguna.
- UI TIDAK membaca/menulis file CSV secara langsung.
- Seluruh manipulasi data (pencarian, pengurutan, penambahan, penghapusan, filter)
  didelegasikan ke class TugasService (Dependency Injection).
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from services import TugasService


class DeadlineWoiUI:
    """
    Kelas antarmuka pengguna berbasis Tkinter untuk aplikasi DeadlineWoi.
    """

    def __init__(self, root: tk.Tk, service: Optional[TugasService] = None) -> None:
        """
        Inisialisasi jendela utama dan komponen UI.

        Parameter
        ---------
        root    : Objek root tk.Tk.
        service : Objek TugasService. Jika None, otomatis membuat instance baru.
        """
        self.root = root
        self.root.title("DeadlineWoi — Manajemen Tugas Kuliah")
        self.root.geometry("980x600")
        self.root.minsize(850, 500)

        # Menerapkan Dependency Injection untuk modularitas
        self.service = service if service is not None else TugasService()

        # Konfigurasi style Tkinter ttk
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Bangun komponen UI
        self._buat_komponen()

        # Muat data pertama kali
        self.segarkan_tabel()

    def _buat_komponen(self) -> None:
        """Menyusun seluruh tata letak widget (layout) pada jendela."""
        # Frame Kontainer Utama
        kontainer = ttk.Frame(self.root, padding="12")
        kontainer.pack(fill=tk.BOTH, expand=True)

        # ---------------- 1. Header Judul ----------------
        header_frame = ttk.Frame(kontainer)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        lbl_judul = ttk.Label(
            header_frame,
            text="📝 DeadlineWoi",
            font=("Segoe UI", 16, "bold"),
            foreground="#1e3a8a",
        )
        lbl_judul.pack(side=tk.LEFT)

        lbl_subjudul = ttk.Label(
            header_frame,
            text="Aplikasi Manajemen Tugas & Deadline Kuliah",
            font=("Segoe UI", 9, "italic"),
            foreground="#64748b",
        )
        lbl_subjudul.pack(side=tk.LEFT, padx=10, pady=4)

        # ---------------- 2. Bar Navigasi, Pencarian & Filter ----------------
        filter_frame = ttk.LabelFrame(kontainer, text=" Navigasi & Filter Data ", padding="8")
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        # Pencarian
        ttk.Label(filter_frame, text="Cari:").grid(row=0, column=0, padx=(0, 4), sticky=tk.W)
        self.entry_cari = ttk.Entry(filter_frame, width=20)
        self.entry_cari.grid(row=0, column=1, padx=4, sticky=tk.W)
        self.entry_cari.bind("<Return>", lambda event: self.aksi_cari())

        btn_cari = ttk.Button(filter_frame, text="🔍 Cari", command=self.aksi_cari)
        btn_cari.grid(row=0, column=2, padx=4)

        # Filter Status
        ttk.Label(filter_frame, text="Status:").grid(row=0, column=3, padx=(12, 4))
        self.combo_status = ttk.Combobox(
            filter_frame, values=["Semua", "Belum", "Proses", "Selesai"], state="readonly", width=10
        )
        self.combo_status.current(0)
        self.combo_status.grid(row=0, column=4, padx=4)
        self.combo_status.bind("<<ComboboxSelected>>", lambda event: self.aksi_filter_status())

        # Pengurutan (Sorting)
        ttk.Label(filter_frame, text="Urutkan:").grid(row=0, column=5, padx=(12, 4))
        self.combo_urutkan = ttk.Combobox(
            filter_frame,
            values=["Deadline Terdekat", "Prioritas Utama", "Bobot Jam Terbesar", "Judul (A-Z)"],
            state="readonly",
            width=18,
        )
        self.combo_urutkan.current(0)
        self.combo_urutkan.grid(row=0, column=6, padx=4)

        btn_urut = ttk.Button(filter_frame, text="Urutkan", command=self.aksi_urutkan)
        btn_urut.grid(row=0, column=7, padx=4)

        btn_reset = ttk.Button(filter_frame, text="🔄 Segarkan / Reset", command=self.segarkan_tabel)
        btn_reset.grid(row=0, column=8, padx=(12, 0))

        # ---------------- 3. Tabel Data (Treeview) ----------------
        tabel_frame = ttk.Frame(kontainer)
        tabel_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        kolom = ("id", "judul", "mata_kuliah", "kategori", "deadline", "bobot_jam", "prioritas", "status")
        self.tabel = ttk.Treeview(tabel_frame, columns=kolom, show="headings", selectmode="browse")

        # Definisi Header Kolom
        self.tabel.heading("id", text="ID")
        self.tabel.heading("judul", text="Judul Tugas")
        self.tabel.heading("mata_kuliah", text="Mata Kuliah")
        self.tabel.heading("kategori", text="Kategori")
        self.tabel.heading("deadline", text="Deadline")
        self.tabel.heading("bobot_jam", text="Est. Jam")
        self.tabel.heading("prioritas", text="Prioritas")
        self.tabel.heading("status", text="Status")

        # Lebar Kolom
        self.tabel.column("id", width=60, anchor=tk.CENTER)
        self.tabel.column("judul", width=220, anchor=tk.W)
        self.tabel.column("mata_kuliah", width=180, anchor=tk.W)
        self.tabel.column("kategori", width=80, anchor=tk.CENTER)
        self.tabel.column("deadline", width=95, anchor=tk.CENTER)
        self.tabel.column("bobot_jam", width=75, anchor=tk.CENTER)
        self.tabel.column("prioritas", width=75, anchor=tk.CENTER)
        self.tabel.column("status", width=85, anchor=tk.CENTER)

        # Scrollbar vertikal
        scrollbar = ttk.Scrollbar(tabel_frame, orient=tk.VERTICAL, command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=scrollbar.set)

        self.tabel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ---------------- 4. Tombol Aksi Bawah ----------------
        aksi_frame = ttk.Frame(kontainer)
        aksi_frame.pack(fill=tk.X, pady=(0, 8))

        btn_tambah = ttk.Button(aksi_frame, text="➕ Tambah Tugas Baru", command=self.dialog_tambah_tugas)
        btn_tambah.pack(side=tk.LEFT, padx=(0, 6))

        btn_status = ttk.Button(aksi_frame, text="✔ Ubah Status", command=self.dialog_ubah_status)
        btn_status.pack(side=tk.LEFT, padx=6)

        btn_hapus = ttk.Button(aksi_frame, text="🗑 Hapus Tugas", command=self.aksi_hapus)
        btn_hapus.pack(side=tk.LEFT, padx=6)

        # ---------------- 5. Footer Informasi & Agregasi ----------------
        self.lbl_footer = ttk.Label(
            kontainer,
            text="",
            font=("Segoe UI", 9, "bold"),
            foreground="#334155",
        )
        self.lbl_footer.pack(fill=tk.X, pady=(4, 0))

    # ------------------------------------------------------------------ #
    #  Aksi-aksi UI (Event Handlers)
    # ------------------------------------------------------------------ #

    def segarkan_tabel(self, daftar=None) -> None:
        """Mengisi ulang baris tabel Treeview dengan data tugas terbaru."""
        # Bersihkan data lama di tabel
        for baris in self.tabel.get_children():
            self.tabel.delete(baris)

        # Jika daftar tidak diberikan, ambil seluruh data dari service
        if daftar is None:
            self.entry_cari.delete(0, tk.END)
            self.combo_status.current(0)
            daftar = self.service.ambil_semua()

        # Masukkan data ke tabel
        for t in daftar:
            self.tabel.insert(
                "",
                tk.END,
                values=(
                    t.id,
                    t.judul,
                    t.mata_kuliah,
                    t.kategori,
                    t.deadline,
                    f"{t.bobot_jam} jam",
                    f"Tingkat {t.prioritas}",
                    t.status,
                ),
            )

        # Perbarui footer statistik menggunakan fitur *args dari service
        total_jam = self.service.hitung_total_jam(*daftar) if daftar else 0.0
        self.lbl_footer.config(
            text=f"Total Data: {len(daftar)} tugas  |  Estimasi Waktu Pengerjaan: {total_jam:.1f} jam"
        )

    def aksi_cari(self) -> None:
        """Menjalankan pencarian kata kunci pada data tugas."""
        kata_kunci = self.entry_cari.get()
        hasil = self.service.cari_tugas(kata_kunci)
        self.segarkan_tabel(hasil)

    def aksi_filter_status(self) -> None:
        """Menyaring tampilan tabel berdasarkan status tugas (**kwargs)."""
        status_pilihan = self.combo_status.get()
        if status_pilihan == "Semua":
            self.segarkan_tabel(self.service.ambil_semua())
        else:
            hasil = self.service.filter_tugas(status=status_pilihan)
            self.segarkan_tabel(hasil)

    def aksi_urutkan(self) -> None:
        """Mengurutkan tampilan tabel menggunakan fungsi lambda di service."""
        pilihan = self.combo_urutkan.get()
        daftar_sekarang = self._ambil_tugas_dari_tabel_saat_ini()

        if pilihan == "Deadline Terdekat":
            hasil = self.service.urutkan_tugas(daftar=daftar_sekarang, kunci="deadline", menurun=False)
        elif pilihan == "Prioritas Utama":
            hasil = self.service.urutkan_tugas(daftar=daftar_sekarang, kunci="prioritas", menurun=False)
        elif pilihan == "Bobot Jam Terbesar":
            hasil = self.service.urutkan_tugas(daftar=daftar_sekarang, kunci="bobot_jam", menurun=True)
        elif pilihan == "Judul (A-Z)":
            hasil = self.service.urutkan_tugas(daftar=daftar_sekarang, kunci="judul", menurun=False)
        else:
            hasil = daftar_sekarang

        self.segarkan_tabel(hasil)

    def aksi_hapus(self) -> None:
        """Menghapus tugas yang sedang dipilih pada tabel."""
        terpilih = self.tabel.selection()
        if not terpilih:
            messagebox.showwarning("Peringatan", "Pilih salah satu tugas pada tabel terlebih dahulu!")
            return

        item = self.tabel.item(terpilih[0])
        id_tugas = item["values"][0]
        judul = item["values"][1]

        if messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus tugas '{judul}' ({id_tugas})?"):
            sukses = self.service.hapus_tugas(str(id_tugas))
            if sukses:
                messagebox.showinfo("Sukses", f"Tugas '{id_tugas}' berhasil dihapus.")
                self.segarkan_tabel()
            else:
                messagebox.showerror("Gagal", "Gagal menghapus tugas dari sistem.")

    def dialog_ubah_status(self) -> None:
        """Membuka dialog popup untuk mengubah status tugas terpilih."""
        terpilih = self.tabel.selection()
        if not terpilih:
            messagebox.showwarning("Peringatan", "Pilih salah satu tugas pada tabel terlebih dahulu!")
            return

        item = self.tabel.item(terpilih[0])
        id_tugas = str(item["values"][0])
        status_sekarang = item["values"][7]

        # Jendela Popup
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Ubah Status {id_tugas}")
        dialog.geometry("300x160")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text=f"Tugas: {id_tugas} - {item['values'][1][:20]}...").pack(pady=(12, 6))
        ttk.Label(dialog, text="Pilih Status Baru:").pack(pady=2)

        combo = ttk.Combobox(dialog, values=["Belum", "Proses", "Selesai"], state="readonly")
        combo.set(status_sekarang)
        combo.pack(pady=4)

        def simpan_status():
            status_baru = combo.get()
            try:
                self.service.perbarui_status(id_tugas, status_baru)
                messagebox.showinfo("Sukses", f"Status berhasil diubah menjadi '{status_baru}'!")
                dialog.destroy()
                self.segarkan_tabel()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dialog, text="Simpan", command=simpan_status).pack(pady=10)

    def dialog_tambah_tugas(self) -> None:
        """Membuka form popup dialog untuk menambah tugas baru."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Tambah Tugas Baru")
        dialog.geometry("380x380")
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        # Field Judul
        ttk.Label(frame, text="Judul Tugas:").grid(row=0, column=0, sticky=tk.W, pady=4)
        entry_judul = ttk.Entry(frame, width=28)
        entry_judul.grid(row=0, column=1, pady=4)

        # Field Mata Kuliah
        ttk.Label(frame, text="Mata Kuliah:").grid(row=1, column=0, sticky=tk.W, pady=4)
        entry_mk = ttk.Entry(frame, width=28)
        entry_mk.grid(row=1, column=1, pady=4)

        # Field Kategori
        ttk.Label(frame, text="Kategori:").grid(row=2, column=0, sticky=tk.W, pady=4)
        combo_kat = ttk.Combobox(frame, values=["Kuis", "Tugas", "Proyek", "UTS", "UAS"], state="readonly", width=25)
        combo_kat.current(1)
        combo_kat.grid(row=2, column=1, pady=4)

        # Field Deadline
        ttk.Label(frame, text="Deadline (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W, pady=4)
        entry_dl = ttk.Entry(frame, width=28)
        entry_dl.insert(0, "2026-12-01")
        entry_dl.grid(row=3, column=1, pady=4)

        # Field Bobot Jam
        ttk.Label(frame, text="Est. Jam (angka >= 0):").grid(row=4, column=0, sticky=tk.W, pady=4)
        entry_jam = ttk.Entry(frame, width=28)
        entry_jam.insert(0, "2.0")
        entry_jam.grid(row=4, column=1, pady=4)

        # Field Prioritas
        ttk.Label(frame, text="Prioritas (1-3):").grid(row=5, column=0, sticky=tk.W, pady=4)
        combo_prio = ttk.Combobox(frame, values=["1", "2", "3"], state="readonly", width=25)
        combo_prio.current(0)
        combo_prio.grid(row=5, column=1, pady=4)

        # Field Status
        ttk.Label(frame, text="Status:").grid(row=6, column=0, sticky=tk.W, pady=4)
        combo_st = ttk.Combobox(frame, values=["Belum", "Proses", "Selesai"], state="readonly", width=25)
        combo_st.current(0)
        combo_st.grid(row=6, column=1, pady=4)

        def simpan_tugas():
            data_dict = {
                "id": "",  # ID dibuatkan otomatis oleh service
                "judul": entry_judul.get(),
                "mata_kuliah": entry_mk.get(),
                "kategori": combo_kat.get(),
                "deadline": entry_dl.get(),
                "bobot_jam": entry_jam.get(),
                "prioritas": combo_prio.get(),
                "status": combo_st.get(),
            }
            try:
                # Panggil service untuk validasi dan penambahan
                tugas_baru = self.service.tambah_tugas(data_dict)
                messagebox.showinfo("Sukses", f"Tugas '{tugas_baru.judul}' ({tugas_baru.id}) berhasil ditambahkan!")
                dialog.destroy()
                self.segarkan_tabel()
            except ValueError as e:
                # Tampilkan pesan error validasi ke pengguna tanpa crash
                messagebox.showerror("Validasi Gagal", str(e))

        ttk.Button(frame, text="💾 Simpan Tugas", command=simpan_tugas).grid(row=7, column=0, columnspan=2, pady=16)

    def _ambil_tugas_dari_tabel_saat_ini(self):
        """Helper untuk mengambil objek Tugas dari ID yang sedang tampil di tabel."""
        daftar = []
        for child in self.tabel.get_children():
            id_tugas = str(self.tabel.item(child)["values"][0])
            t = self.service.ambil_berdasarkan_id(id_tugas)
            if t:
                daftar.append(t)
        return daftar


def jalankan_ui():
    """Fungsi pembungkus untuk menjalankan aplikasi UI Tkinter."""
    root = tk.Tk()
    app = DeadlineWoiUI(root)
    root.mainloop()


if __name__ == "__main__":
    jalankan_ui()
