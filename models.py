class Tugas:
    """Mewakili satu tugas kuliah."""

    HEADER = ["id", "judul", "mata_kuliah", "kategori",
              "deadline", "bobot_jam", "prioritas", "status"]

    def __init__(
        self,
        id: str,
        judul: str,
        mata_kuliah: str,
        kategori: str,
        deadline: str,
        bobot_jam: float,
        prioritas: int,
        status: str,
    ) -> None:
        """Menginisialisasi data tugas."""
        self.id = id
        self.judul = judul
        self.mata_kuliah = mata_kuliah
        self.kategori = kategori
        self.deadline = deadline
        self.bobot_jam = bobot_jam
        self.prioritas = prioritas
        self.status = status

    def ke_dict(self) -> dict:
        """Mengubah data tugas menjadi dictionary."""
        return {
            "id": self.id,
            "judul": self.judul,
            "mata_kuliah": self.mata_kuliah,
            "kategori": self.kategori,
            "deadline": self.deadline,
            "bobot_jam": self.bobot_jam,
            "prioritas": self.prioritas,
            "status": self.status,
        }

    @classmethod
    def dari_dict(cls, data: dict) -> "Tugas":
        """Membuat objek tugas dari dictionary."""
        return cls(
            id=data["id"],
            judul=data["judul"],
            mata_kuliah=data["mata_kuliah"],
            kategori=data["kategori"],
            deadline=data["deadline"],
            bobot_jam=float(data["bobot_jam"]),
            prioritas=int(data["prioritas"]),
            status=data["status"],
        )

    def __repr__(self) -> str:
        """Mengembalikan representasi teks dari tugas."""
        return (
            f"Tugas(id={self.id!r}, judul={self.judul!r}, "
            f"deadline={self.deadline!r}, status={self.status!r})"
        )




