# CapstoneModule1

Capstone Module 1 (Python) - Sistem Pengelolaan Menu &amp; Pesanan Restoran

# Deskripsi Project

Aplikasi Manajemen Pemesanan Restoran Berbasis Terminal (CLI) ini adalah sebuah sistem sederhana yang membantu pemilik atau admin restoran mengelola data menu makanan dan pesanan secara efisien.
Aplikasi ini dijalankan di komputer lokal melalui command line/terminal tanpa memerlukan database atau server, dan menampilkan data dengan tampilan tabel yang rapi menggunakan Python.

# Tujuan

- Menyediakan solusi praktis untuk administrasi menu makanan dan pemesanan di restoran, warung, atau cafe dengan workflow yang mudah dipahami.

- Memudahkan pemilik atau admin dalam melakukan pencatatan, pengelolaan, pencarian, serta update data menu dan pesanan.

- Menjamin validasi data (stok, input, status, dsb.) agar pengelolaan pesanan dan stok lebih akurat.

- Menyediakan fitur export data ke file CSV untuk backup, analisis, atau pembuatan laporan sederhana.

- Memberikan dasar aplikasi yang mudah dikembangkan lagi, baik ke web, desktop, ataupun integrasi database.

# Data yang Disimpan
Aplikasi ini menyimpan dua jenis data utama:

1. Menu Makanan (menu_makanan)
- id (integer): ID unik menu
- nama (string): Nama makanan/minuman
- harga (integer): Harga satuan (rupiah, kelipatan 1000)
- stok (integer): Stok menu tersedia

2. Pesanan (pesanan)
- id (integer): ID unik pesanan
- nama_pemesan (string): Nama pelanggan
- items (list): Daftar item yang dipesan, terdiri dari:
  - menu_id (integer): ID menu
  - menu (string): Nama menu
  - jumlah (integer): Jumlah pesanan
  - subtotal (integer): Total harga untuk menu tersebut
- total_harga (integer): Total harga pesanan
- status (string): Status pesanan (Diproses, Selesai, Dibatalkan)
- tanggal (string): Tanggal & waktu pesanan

# Fitur

- **Login Pemilik Toko:** Keamanan akses aplikasi.
- **CRUD Menu & Pesanan:** Tambah, baca, ubah, hapus data menu makanan dan pesanan.
- **Filter/Search:** Cari menu berdasarkan nama, cari pesanan berdasarkan nama pemesan atau status.
- **Export ke CSV:** Simpan data menu & pesanan ke file CSV.
- **Validasi Data:** Nama, stok, harga, status, dan ketersediaan stok otomatis tervalidasi.
- **Tampilan Tabel:** Semua data ditampilkan rapi dengan tabulate.
- **Status & Tanggal Pesanan:** Status selalu terupdate dan tanggal otomatis tersimpan.

# Petunjuk Penggunaan

- Pilih menu CRUD untuk menambah, mengedit, menghapus, atau melihat data menu dan pesanan.

- Gunakan fitur filter untuk mencari menu/pesanan.

- Tambahkan pesanan dengan beberapa menu sekaligus, stok akan otomatis berkurang.

- Export data ke CSV bisa dilakukan kapan saja dari menu Export.

- Data akan hilang jika aplikasi ditutup (belum terintegrasi database), namun data dapat di-backup/export ke CSV.
