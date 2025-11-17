# 🖥️ Sistem Manajemen Aset TI

Aplikasi manajemen aset TI berbasis **Django REST Framework** untuk backend, dan **Vue 3 + Vite + TailwindCSS** untuk frontend.  
Proyek ini dirancang agar ringan, cepat, mudah dipelihara, dan cocok digunakan oleh tim IT untuk mengelola aset laptop, PC, monitor, printer, dan scanner.

---

## ✨ Fitur Utama

### 🔍 Manajemen Aset
- Tambah, ubah, hapus, dan lihat detail aset.
- Mendukung 5 jenis aset TI:
  - Laptop
  - PC
  - Printer
  - Monitor
  - Scanner

### 🧩 Spesifikasi Berdasarkan Jenis
| Jenis Aset  | Spesifikasi |
|-------------|-------------|
| Laptop / PC | RAM, Storage, Processor, OS |
| Printer     | Berwarna atau tidak |
| Monitor     | Ukuran (inch) |
| Scanner     | DPI & Tipe koneksi |

### 📋 Fitur Table
- Sorting per kolom (ASC/DESC)
- Pencarian cepat (debounce)
- Pagination
- Tampilan mobile (responsive)
- Aksi cepat: Lihat • Ubah • Hapus

---

## 📁 Struktur Folder
aset/
├── backend/
│ ├── assets/
│ ├── project/
│ └── manage.py
├── frontend/
├── .gitignore
└── README.md


---

# 🛠 Instalasi & Menjalankan Project

## 1️⃣ Clone Repository
```bash
git clone https://github.com/<username>/aset-management.git
cd aset-management

