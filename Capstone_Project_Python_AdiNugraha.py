# CAPSTONE PROJECT 1 - Sistem Pengelolaan Menu & Pesanan Restoran
# ADI NUGRAHA JCDSOH 01

import os
import csv
from tabulate import tabulate
from datetime import datetime

# ========== KONFIGURASI DAN DATA AWAL ==========

USER = "owner"
PASS = "12345"
STATUS_PESANAN = ["Diproses", "Selesai", "Dibatalkan"]

menu_makanan = [
    {"id": 1, "nama": "Nasi Goreng", "harga": 20000, "stok": 10},
    {"id": 2, "nama": "Mie Ayam", "harga": 15000, "stok": 8},
    {"id": 3, "nama": "Sate Ayam", "harga": 25000, "stok": 12},
    {"id": 4, "nama": "Bakso", "harga": 18000, "stok": 15},
    {"id": 5, "nama": "Ayam Geprek", "harga": 22000, "stok": 10}
]

pesanan = [
    {
        "id": 1,
        "nama_pemesan": "Adi",
        "items": [
            {"menu_id": 1, "menu": "Nasi Goreng", "jumlah": 2, "subtotal": 40000}
        ],
        "total_harga": 40000,
        "status": "Diproses",
        "tanggal": "2024-06-15 12:34:56"
    },
    {
        "id": 2,
        "nama_pemesan": "Budi",
        "items": [
            {"menu_id": 3, "menu": "Sate Ayam", "jumlah": 1, "subtotal": 25000}
        ],
        "total_harga": 25000,
        "status": "Selesai",
        "tanggal": "2024-06-15 13:10:11"
    }
]

# ========== UTILITAS DASAR ==========

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_nama_valid(nama):
    return all((c.isalpha() or c.isspace()) for c in nama) and nama.strip() != ""

def input_int(prompt, allow_zero=False, back_option=True):
    while True:
        val = input(prompt).strip()
        if back_option and val == "0":
            return None
        try:
            val_int = int(val)
            if allow_zero:
                if val_int < 0:
                    raise ValueError
            else:
                if val_int <= 0:
                    raise ValueError
            return val_int
        except:
            if allow_zero:
                print("Input harus angka bulat >= 0.")
            else:
                print("Input harus angka bulat > 0.")

def tampilkan_tabel(data, header="keys", title=None):
    if title:
        print(f"=== {title} ===")
    if data:
        print(tabulate(data, headers=header, tablefmt="grid"))
    else:
        print("Data tidak tersedia.")

# ========== LOGIN ==========

def login():
    while True:
        clear()
        print("=== LOGIN PEMILIK TOKO ===")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        if username == USER and password == PASS:
            clear()
            return True
        else:
            print("\nLogin gagal! Username/password salah.")
            input("Tekan Enter untuk mencoba lagi...")

# ========== CREATE ==========

def tambah_menu_makanan_batch():
    batch = []
    while True:
        clear()
        if menu_makanan:
            tampilkan_tabel(menu_makanan, title="List Menu yang Sudah Ada")
        if batch:
            tampilkan_tabel(batch, title="Data yang Akan Ditambahkan")
        print("\nIsi data menu (atau ketik 0 untuk kembali)")
        nama = input("Nama menu: ").strip()
        if nama == "0":
            clear()
            break
        if not nama:
            print("Nama menu tidak boleh kosong!")
            input("Tekan Enter untuk lanjut...")
            continue
        if any(m['nama'].lower() == nama.lower() for m in menu_makanan + batch):
            print("Nama menu sudah ada, silakan pilih nama lain!")
            input("Tekan Enter untuk lanjut...")
            continue
        harga = input_int("Harga: ")
        if harga is None:
            clear()
            break
        stok = input_int("Stok: ", allow_zero=True)
        if stok is None:
            clear()
            break
        id_baru = max([m['id'] for m in menu_makanan + batch], default=0) + 1
        data_baru = {"id": id_baru, "nama": nama, "harga": harga, "stok": stok}
        batch.append(data_baru)
        lanjut = input("Tambah menu lagi? (y/n): ").strip().lower()
        if lanjut != "y":
            break
    if batch:
        clear()
        tampilkan_tabel(batch, title="Konfirmasi Data yang Akan Ditambahkan")
        simpan = input("Simpan semua data di atas? (y/n): ").strip().lower()
        if simpan == "y":
            menu_makanan.extend(batch)
            print("Semua menu berhasil ditambahkan!")
        else:
            print("Data batal disimpan.")
        input("Tekan Enter untuk kembali ke menu create...")
    clear()

def tambah_pesanan_batch_multi():
    batch = []
    while True:
        clear()
        tampilkan_tabel(menu_makanan, title="List Menu Makanan yang Tersedia")
        if batch:
            preview_batch = []
            for p in batch:
                item_rinci = '; '.join([f'{i["menu"]} x{i["jumlah"]}' for i in p['items']])
                preview_batch.append({
                    "ID": p["id"],
                    "Nama Pemesan": p["nama_pemesan"],
                    "Menu": item_rinci,
                    "Total": p["total_harga"],
                    "Status": p["status"],
                    "Tanggal": p["tanggal"]
                })
            tampilkan_tabel(preview_batch, title="Data Pesanan yang Akan Ditambahkan")
        print("\nIsi data pesanan (atau ketik 0 untuk kembali)")
        nama_pemesan = input("Nama pemesan: ").strip()
        if nama_pemesan == "0":
            clear()
            break
        if not is_nama_valid(nama_pemesan):
            print("Nama pemesan hanya boleh huruf dan spasi!")
            input("Tekan Enter untuk lanjut...")
            continue
        items = []
        while True:
            clear()
            print(f"Pemesan: {nama_pemesan}")
            if items:
                tampilkan_tabel(items, title="Item Sementara")
            tampilkan_tabel(menu_makanan, title="MENU MAKANAN YANG TERSEDIA")
            print("Ketik 0 jika sudah selesai memilih menu")
            id_menu = input_int("Masukkan ID menu yang dipesan: ", back_option=True)
            if id_menu is None:
                if items:
                    break
                else:
                    print("Minimal satu menu harus dipilih.")
                    input("Tekan Enter untuk lanjut...")
                    continue
            menu_item = next((m for m in menu_makanan if m["id"] == id_menu), None)
            if not menu_item:
                print("ID menu tidak ditemukan!")
                input("Tekan Enter untuk lanjut...")
                continue
            jumlah = input_int("Jumlah porsi: ", back_option=False)
            total_batch = sum(
                i['jumlah']
                for p in batch for i in p['items'] if i['menu_id'] == menu_item['id']
            )
            total_tmp = sum(i['jumlah'] for i in items if i['menu_id'] == menu_item['id'])
            stok_tersedia = menu_item['stok'] - total_batch - total_tmp
            if jumlah > stok_tersedia:
                print(f"Stok tidak cukup! Sisa stok (setelah batch): {stok_tersedia}")
                input("Tekan Enter untuk lanjut...")
                continue
            items.append({
                "menu_id": menu_item["id"],
                "menu": menu_item["nama"],
                "jumlah": jumlah,
                "subtotal": menu_item["harga"] * jumlah
            })
            tampilkan_tabel(items, title="Data Pesanan Sementara")
            input("Tekan Enter untuk lanjut menambah menu/selesai...")

        total_harga = sum(i['subtotal'] for i in items)
        print("\nPilih status pesanan:")
        status_menu_options = [[str(idx+1), stat] for idx, stat in enumerate(STATUS_PESANAN)]
        print(tabulate(status_menu_options, headers=["No", "Status"], tablefmt="grid"))
        pilih_status = input_int(f"Pilih status (1-{len(STATUS_PESANAN)}, default 1): ", allow_zero=False, back_option=False)
        if pilih_status and 1 <= pilih_status <= len(STATUS_PESANAN):
            status = STATUS_PESANAN[pilih_status - 1]
        else:
            status = STATUS_PESANAN[0]
        tanggal_pesanan = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        id_pesanan = max([p['id'] for p in pesanan + batch], default=0) + 1
        data_pesanan = {
            "id": id_pesanan,
            "nama_pemesan": nama_pemesan,
            "items": items,
            "total_harga": total_harga,
            "status": status,
            "tanggal": tanggal_pesanan
        }
        clear()
        tampilkan_tabel(items, title="Detail Item Pesanan Baru")
        print(f"Nama Pemesan: {nama_pemesan}")
        print(f"Total Harga : {total_harga}")
        print(f"Status      : {status}")
        print(f"Tanggal     : {tanggal_pesanan}")
        konfirmasi = input("\nSimpan pesanan ini? (y/n): ").strip().lower()
        if konfirmasi == "y":
            batch.append(data_pesanan)
        else:
            print("Pesanan batal ditambahkan.")
            input("Tekan Enter untuk lanjut...")
        lanjut = input("Tambah pesanan lagi? (y/n): ").strip().lower()
        if lanjut != "y":
            break

    if batch:
        clear()
        preview_batch = []
        for p in batch:
            item_rinci = '; '.join([f'{i["menu"]} x{i["jumlah"]}' for i in p['items']])
            preview_batch.append({
                "ID": p["id"],
                "Nama Pemesan": p["nama_pemesan"],
                "Menu": item_rinci,
                "Total": p["total_harga"],
                "Status": p["status"],
                "Tanggal": p["tanggal"]
            })
        tampilkan_tabel(preview_batch, title="Konfirmasi Pesanan yang Akan Disimpan")
        simpan = input("Simpan semua pesanan di atas? (y/n): ").strip().lower()
        if simpan == "y":
            for pesanan_baru in batch:
                pesanan.append(pesanan_baru)
                for i in pesanan_baru["items"]:
                    menu_item = next((m for m in menu_makanan if m["id"] == i["menu_id"]), None)
                    if menu_item:
                        menu_item["stok"] -= i["jumlah"]
            print("Semua pesanan berhasil ditambahkan!")
        else:
            print("Pesanan batal disimpan.")
        input("Tekan Enter untuk kembali ke menu create...")
    clear()

# ========== READ & FILTER ==========

def tampilkan_data_menu(wait_input=True):
    clear()
    tampilkan_tabel(menu_makanan, title="DATA MENU MAKANAN")
    if wait_input:
        input("\nTekan Enter untuk kembali...")
        clear()

def tampilkan_data_pesanan():
    clear()
    data = []
    for p in pesanan:
        items = "; ".join([f"{i['menu']} x{i['jumlah']}" for i in p['items']])
        data.append({
            "ID": p["id"],
            "Nama Pemesan": p["nama_pemesan"],
            "Menu": items,
            "Total": p["total_harga"],
            "Status": p["status"],
            "Tanggal": p.get("tanggal", "-")
        })
    tampilkan_tabel(data, title="DATA PESANAN")
    input("\nTekan Enter untuk kembali...")
    clear()

def filter_menu_makanan():
    clear()
    keyword = input("Cari menu berdasarkan nama (kosongkan untuk tampil semua): ").strip().lower()
    if keyword:
        hasil = [m for m in menu_makanan if keyword in m["nama"].lower()]
    else:
        hasil = menu_makanan
    tampilkan_tabel(hasil, title="HASIL FILTER MENU")
    input("\nTekan Enter untuk kembali...")
    clear()

def filter_pesanan():
    clear()
    print("Filter berdasarkan:")
    filter_opsi = [
        ["1", "Nama Pemesan"],
        ["2", "Status Pesanan"],
        ["3", "Tampilkan Semua"]
    ]
    print(tabulate(filter_opsi, headers=["No", "Opsi"], tablefmt="grid"))
    pilih = input("Pilih filter: ").strip()
    hasil = pesanan
    if pilih == "1":
        nama = input("Nama pemesan: ").strip().lower()
        hasil = [p for p in pesanan if nama in p["nama_pemesan"].lower()]
    elif pilih == "2":
        print("Status: Diproses / Selesai / Dibatalkan")
        status = input("Status: ").strip().capitalize()
        hasil = [p for p in pesanan if p["status"] == status]
    data = []
    for p in hasil:
        items = "; ".join([f"{i['menu']} x{i['jumlah']}" for i in p['items']])
        data.append({
            "ID": p["id"],
            "Nama Pemesan": p["nama_pemesan"],
            "Menu": items,
            "Total": p["total_harga"],
            "Status": p["status"],
            "Tanggal": p.get("tanggal", "-")
        })
    tampilkan_tabel(data, title="HASIL FILTER PESANAN")
    input("\nTekan Enter untuk kembali...")
    clear()

# ========== UPDATE ==========

def update_menu_makanan():
    while True:
        clear()
        tampilkan_tabel(menu_makanan, title="DATA MENU MAKANAN (Update)")
        id_menu = input_int("Masukkan ID menu yang akan diupdate (atau 0 untuk kembali): ", back_option=True)
        if id_menu is None:
            clear()
            break
        menu = next((m for m in menu_makanan if m["id"] == id_menu), None)
        if not menu:
            print("ID menu tidak ditemukan!")
            input("Tekan Enter untuk lanjut...")
            continue
        print(f"\nEdit data menu: {menu['nama']} (ID: {menu['id']})")
        nama_baru = input(f"Nama baru [{menu['nama']}]: ").strip()
        if nama_baru and any(m['nama'].lower() == nama_baru.lower() and m['id'] != id_menu for m in menu_makanan):
            print("Nama menu sudah ada, tidak boleh duplikat.")
            input("Tekan Enter untuk lanjut...")
            continue
        harga_baru = input(f"Harga baru [{menu['harga']}]: ").strip()
        stok_baru = input(f"Stok baru [{menu['stok']}]: ").strip()
        print("\nKonfirmasi perubahan:")
        print(f"Nama   : {nama_baru if nama_baru else menu['nama']}")
        print(f"Harga  : {harga_baru if harga_baru else menu['harga']}")
        print(f"Stok   : {stok_baru if stok_baru else menu['stok']}")
        konfirm = input("Simpan perubahan? (y/n): ").strip().lower()
        if konfirm == "y":
            if nama_baru:
                menu['nama'] = nama_baru
            if harga_baru:
                try:
                    harga_baru = int(harga_baru)
                    if harga_baru <= 0:
                        raise ValueError
                    menu['harga'] = harga_baru
                except:
                    print("Harga tidak valid, data tidak diubah.")
            if stok_baru:
                try:
                    stok_baru = int(stok_baru)
                    if stok_baru < 0:
                        raise ValueError
                    menu['stok'] = stok_baru
                except:
                    print("Stok tidak valid, data tidak diubah.")
            print("Data menu berhasil diupdate!")
        else:
            print("Perubahan dibatalkan.")
        input("Tekan Enter untuk kembali...")
        break

def update_pesanan():
    while True:
        clear()
        data = []
        for p in pesanan:
            items = "; ".join([f"{i['menu']} x{i['jumlah']}" for i in p['items']])
            data.append({
                "ID": p["id"],
                "Nama Pemesan": p["nama_pemesan"],
                "Menu": items,
                "Total": p["total_harga"],
                "Status": p["status"],
                "Tanggal": p.get("tanggal", "-")
            })
        tampilkan_tabel(data, title="DATA PESANAN (Update)")
        id_pes = input_int("Masukkan ID pesanan yang akan diupdate (atau 0 untuk kembali): ", back_option=True)
        if id_pes is None:
            clear()
            break
        pes = next((p for p in pesanan if p["id"] == id_pes), None)
        if not pes:
            print("ID pesanan tidak ditemukan!")
            input("Tekan Enter untuk lanjut...")
            continue
        print(f"\nEdit pesanan untuk: {pes['nama_pemesan']} (ID: {pes['id']})")
        nama_baru = input(f"Nama pemesan baru [{pes['nama_pemesan']}]: ").strip()
        if nama_baru and not is_nama_valid(nama_baru):
            print("Nama hanya boleh huruf dan spasi.")
            input("Tekan Enter untuk lanjut...")
            continue
        tambah_item = input("Tambah menu ke pesanan? (y/n): ").strip().lower()
        items_baru = pes['items'].copy()
        total_harga_baru = pes['total_harga']
        if tambah_item == "y":
            while True:
                tampilkan_tabel(menu_makanan, title="MENU MAKANAN UNTUK DITAMBAH")
                id_menu = input_int("ID menu yang ingin ditambahkan (atau 0 untuk selesai): ", back_option=True)
                if id_menu is None:
                    break
                menu_item = next((m for m in menu_makanan if m["id"] == id_menu), None)
                if not menu_item:
                    print("ID menu tidak ditemukan!")
                    continue
                jumlah = input_int("Jumlah porsi: ")
                stok_tersedia = menu_item['stok']
                if jumlah > stok_tersedia:
                    print(f"Stok tidak cukup! Sisa stok: {stok_tersedia}")
                    continue
                existing = next((i for i in items_baru if i['menu_id'] == id_menu), None)
                if existing:
                    existing['jumlah'] += jumlah
                    existing['subtotal'] += menu_item['harga'] * jumlah
                else:
                    items_baru.append({
                        "menu_id": menu_item["id"],
                        "menu": menu_item["nama"],
                        "jumlah": jumlah,
                        "subtotal": menu_item["harga"] * jumlah
                    })
                menu_item['stok'] -= jumlah
                total_harga_baru += menu_item['harga'] * jumlah
                print("Menu berhasil ditambah ke pesanan.")
        print("\nPilih status pesanan:")
        status_menu_options = [[str(idx+1), stat] for idx, stat in enumerate(STATUS_PESANAN)]
        print(tabulate(status_menu_options, headers=["No", "Status"], tablefmt="grid"))
        status_idx = input_int(f"Pilih status (1-{len(STATUS_PESANAN)}, default {STATUS_PESANAN.index(pes['status'])+1}): ", allow_zero=False, back_option=False)
        if status_idx and 1 <= status_idx <= len(STATUS_PESANAN):
            status_baru = STATUS_PESANAN[status_idx-1]
        else:
            status_baru = pes['status']
        clear()
        print("Konfirmasi perubahan pesanan:")
        tampilkan_tabel(items_baru, title="Pesanan Baru")
        print(f"Nama Pemesan: {nama_baru if nama_baru else pes['nama_pemesan']}")
        print(f"Total Harga : {total_harga_baru}")
        print(f"Status      : {status_baru}")
        konfirm = input("Simpan perubahan? (y/n): ").strip().lower()
        if konfirm == "y":
            if nama_baru:
                pes['nama_pemesan'] = nama_baru
            pes['items'] = items_baru
            pes['total_harga'] = total_harga_baru
            pes['status'] = status_baru
            print("Data pesanan berhasil diupdate!")
        else:
            print("Perubahan dibatalkan.")
        input("Tekan Enter untuk kembali...")
        break

# ========== DELETE ==========

def delete_menu_makanan():
    while True:
        clear()
        tampilkan_tabel(menu_makanan, title="DATA MENU MAKANAN (Delete)")
        id_menu = input_int("Masukkan ID menu yang akan dihapus (atau 0 untuk kembali): ", back_option=True)
        if id_menu is None:
            clear()
            break
        menu = next((m for m in menu_makanan if m["id"] == id_menu), None)
        if not menu:
            print("ID menu tidak ditemukan!")
            input("Tekan Enter untuk lanjut...")
            continue
        sedang_dipesan = any(id_menu in [i['menu_id'] for i in p['items']] for p in pesanan)
        if sedang_dipesan:
            print("Menu ini masih ada dalam pesanan. Tidak bisa dihapus.")
            input("Tekan Enter untuk kembali...")
            continue
        print(f"Yakin ingin menghapus menu: {menu['nama']} (ID: {menu['id']}) ?")
        konfirm = input("Ketik 'YA' untuk konfirmasi hapus: ").strip().upper()
        if konfirm == "YA":
            menu_makanan.remove(menu)
            print("Menu berhasil dihapus.")
        else:
            print("Penghapusan dibatalkan.")
        input("Tekan Enter untuk kembali...")
        break

def delete_pesanan():
    while True:
        clear()
        data = []
        for p in pesanan:
            items = "; ".join([f"{i['menu']} x{i['jumlah']}" for i in p['items']])
            data.append({
                "ID": p["id"],
                "Nama Pemesan": p["nama_pemesan"],
                "Menu": items,
                "Total": p["total_harga"],
                "Status": p["status"],
                "Tanggal": p.get("tanggal", "-")
            })
        tampilkan_tabel(data, title="DATA PESANAN (Delete)")
        id_pes = input_int("Masukkan ID pesanan yang akan dihapus (atau 0 untuk kembali): ", back_option=True)
        if id_pes is None:
            clear()
            break
        pes = next((p for p in pesanan if p["id"] == id_pes), None)
        if not pes:
            print("ID pesanan tidak ditemukan!")
            input("Tekan Enter untuk lanjut...")
            continue
        print(f"Yakin ingin menghapus pesanan untuk: {pes['nama_pemesan']} (ID: {pes['id']}) ?")
        konfirm = input("Ketik 'YA' untuk konfirmasi hapus: ").strip().upper()
        if konfirm == "YA":
            for i in pes['items']:
                menu_item = next((m for m in menu_makanan if m["id"] == i["menu_id"]), None)
                if menu_item:
                    menu_item['stok'] += i['jumlah']
            pesanan.remove(pes)
            print("Pesanan berhasil dihapus dan stok dikembalikan.")
        else:
            print("Penghapusan dibatalkan.")
        input("Tekan Enter untuk kembali...")
        break

# ========== SUBMENU CRUD ==========

def sub_menu_create():
    while True:
        clear()
        sub_menu_options = [
            ["1", "Tambah Menu Makanan"],
            ["2", "Tambah Pesanan"],
            ["3", "Kembali ke Menu Utama"]
        ]
        print(tabulate(sub_menu_options, headers=["No", "Submenu Create"], tablefmt="grid"))
        pilih = input("Pilih menu: ").strip()
        if pilih == '1':
            tambah_menu_makanan_batch()
        elif pilih == '2':
            tambah_pesanan_batch_multi()
        elif pilih == '3':
            clear()
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk kembali...")
            clear()

def sub_menu_read():
    while True:
        clear()
        sub_menu_options = [
            ["1", "Lihat Menu Makanan"],
            ["2", "Lihat Data Pesanan"],
            ["3", "Filter Menu"],
            ["4", "Filter Pesanan"],
            ["5", "Kembali ke Menu Utama"]
        ]
        print(tabulate(sub_menu_options, headers=["No", "Submenu Read"], tablefmt="grid"))
        pilih = input("Pilih menu: ").strip()
        if pilih == '1':
            tampilkan_data_menu()
        elif pilih == '2':
            tampilkan_data_pesanan()
        elif pilih == '3':
            filter_menu_makanan()
        elif pilih == '4':
            filter_pesanan()
        elif pilih == '5':
            clear()
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk kembali...")
            clear()

def sub_menu_update():
    while True:
        clear()
        sub_menu_options = [
            ["1", "Update Menu Makanan"],
            ["2", "Update Pesanan"],
            ["3", "Kembali ke Menu Utama"]
        ]
        print(tabulate(sub_menu_options, headers=["No", "Submenu Update"], tablefmt="grid"))
        pilih = input("Pilih menu: ").strip()
        if pilih == '1':
            update_menu_makanan()
        elif pilih == '2':
            update_pesanan()
        elif pilih == '3':
            clear()
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk kembali...")
            clear()

def sub_menu_delete():
    while True:
        clear()
        sub_menu_options = [
            ["1", "Delete Menu Makanan"],
            ["2", "Delete Pesanan"],
            ["3", "Kembali ke Menu Utama"]
        ]
        print(tabulate(sub_menu_options, headers=["No", "Submenu Delete"], tablefmt="grid"))
        pilih = input("Pilih menu: ").strip()
        if pilih == '1':
            delete_menu_makanan()
        elif pilih == '2':
            delete_pesanan()
        elif pilih == '3':
            clear()
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk kembali...")
            clear()

def sub_menu_export():
    while True:
        clear()
        sub_menu_options = [
            ["1", "Export Data Menu ke CSV"],
            ["2", "Export Data Pesanan ke CSV"],
            ["3", "Kembali ke Menu Utama"]
        ]
        print(tabulate(sub_menu_options, headers=["No", "Export Data"], tablefmt="grid"))
        pilih = input("Pilih menu: ").strip()
        if pilih == '1':
            export_menu_to_csv()
        elif pilih == '2':
            export_pesanan_to_csv()
        elif pilih == '3':
            clear()
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk kembali...")
            clear()

# ========== EXPORT KE CSV ==========

def export_menu_to_csv():
    clear()
    filename = input("Nama file output (misal: menu.csv): ").strip()
    if not filename:
        print("Nama file tidak boleh kosong!")
        input("Tekan Enter untuk kembali...")
        return
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["id", "nama", "harga", "stok"])
            writer.writeheader()
            for m in menu_makanan:
                writer.writerow(m)
        print(f"Data menu berhasil diexport ke {filename}")
    except Exception as e:
        print(f"Export gagal: {e}")
    input("Tekan Enter untuk kembali...")

def export_pesanan_to_csv():
    clear()
    filename = input("Nama file output (misal: pesanan.csv): ").strip()
    if not filename:
        print("Nama file tidak boleh kosong!")
        input("Tekan Enter untuk kembali...")
        return
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["id", "nama_pemesan", "menu_dipesan", "total_harga", "status", "tanggal"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for p in pesanan:
                menu_str = "; ".join([f"{i['menu']} x{i['jumlah']}" for i in p['items']])
                writer.writerow({
                    "id": p["id"],
                    "nama_pemesan": p["nama_pemesan"],
                    "menu_dipesan": menu_str,
                    "total_harga": p["total_harga"],
                    "status": p["status"],
                    "tanggal": p["tanggal"]
                })
        print(f"Data pesanan berhasil diexport ke {filename}")
    except Exception as e:
        print(f"Export gagal: {e}")
    input("Tekan Enter untuk kembali...")

# ========== MENU UTAMA ==========

def main_menu():
    while True:
        clear()
        print("=== Sistem Pengelolaan Menu & Pesanan Restoran ===")
        main_menu_options = [
            ["1", "Create (Tambah Data)"],
            ["2", "Read (Lihat Data)"],
            ["3", "Update (Ubah Data)"],
            ["4", "Delete (Hapus Data)"],
            ["5", "Export ke CSV"],
            ["6", "Exit"]
        ]
        print(tabulate(main_menu_options, headers=["No", "Menu Utama"], tablefmt="grid"))
        pilihan = input("Pilih menu: ").strip()
        if pilihan == '1':
            sub_menu_create()
        elif pilihan == '2':
            sub_menu_read()
        elif pilihan == '3':
            sub_menu_update()
        elif pilihan == '4':
            sub_menu_delete()
        elif pilihan == '5':
            sub_menu_export()
        elif pilihan == '6':
            clear()
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!\n")
            input("Tekan Enter untuk kembali...")
            clear()

# ========== ENTRY POINT ==========

if __name__ == "__main__":
    while not login():
        pass
    main_menu()
