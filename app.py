import csv
import os

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedListReservasi:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

# ==========================================
# 2. SISTEM UTAMA RESERVASI FUTSAL
# ==========================================
class SistemFutsal:
    def __init__(self):
        self.file_lapangan = 'lapangan.csv'
        self.file_reservasi = 'reservasi.csv'
        self.inisialisasi_database()
        
    def inisialisasi_database(self):
        # Buat file master lapangan jika belum ada
        if not os.path.exists(self.file_lapangan):
            with open(self.file_lapangan, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id_lapangan', 'nama_lapangan', 'jam', 'status'])
                writer.writerow(['LP01', 'Lapangan Vinyl', '15:00', 'Kosong'])
                writer.writerow(['LP01', 'Lapangan Vinyl', '16:00', 'Kosong'])
                writer.writerow(['LP02', 'Lapangan Rumput', '15:00', 'Kosong'])
                writer.writerow(['LP02', 'Lapangan Rumput', '16:00', 'Kosong'])

        # Buat file reservasi jika belum ada
        if not os.path.exists(self.file_reservasi):
            with open(self.file_reservasi, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id_reservasi', 'nama_penyewa', 'id_lapangan', 'jam', 'total_bayar'])

    # --- C / CREATE: Membuat Reservasi Baru ---
    def buat_reservasi(self):
        print("\n=== BUAT RESERVASI BARU ===")
        self.lihat_lapangan()
        
        id_lapangan = input("Masukkan ID Lapangan yang dipilih: ").upper()
        jam = input("Masukkan Jam (contoh 15:00): ")
        
        lapangan_ditemukan = False
        data_lapangan = []
        
        with open(self.file_lapangan, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['id_lapangan'] == id_lapangan and row['jam'] == jam:
                    if row['status'] == 'Kosong':
                        lapangan_ditemukan = True
                        row['status'] = 'Dipesan'
                    else:
                        print("Maaf, lapangan pada jam tersebut sudah dipesan!")
                        return
                data_lapangan.append(row)
                
        if not lapangan_ditemukan:
            print("ID Lapangan atau Jam tidak valid!")
            return

        nama = input("Masukkan Nama Penyewa: ")
        harga = 150000
        
        id_res = f"RES{len(self.load_reservasi_to_linked_list().to_list()) + 1:03d}"
        
        with open(self.file_reservasi, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([id_res, nama, id_lapangan, jam, harga])
            
        with open(self.file_lapangan, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id_lapangan', 'nama_lapangan', 'jam', 'status'])
            writer.writeheader()
            writer.writerows(data_lapangan)
            
        print(f"✓ Reservasi Berhasil! ID Anda: {id_res}")

    # --- R / READ: Membaca Data Lapangan & Reservasi ---
    def lihat_lapangan(self):
        print("\n--- DAFTAR KETERSEDIAAN LAPANGAN ---")
        print(f"{'ID':<6} | {'Nama Lapangan':<20} | {'Jam':<6} | {'Status':<10}")
        print("-" * 50)
        with open(self.file_lapangan, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                print(f"{row['id_lapangan']:<6} | {row['nama_lapangan']:<20} | {row['jam']:<6} | {row['status']:<10}")

    def load_reservasi_to_linked_list(self):
        ll = LinkedListReservasi()
        with open(self.file_reservasi, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ll.append(row)
        return ll

    # --- IMPLEMENTASI ALGORITMA SEARCHING (Linear Search) ---
    def cari_reservasi(self):
        print("\n=== CARI DATA RESERVASI ===")
        nama_cari = input("Masukkan Nama Penyewa yang dicari: ").lower()
        
        ll = self.load_reservasi_to_linked_list()
        daftar_res = ll.to_list()
        
        ditemukan = False
        print(f"\n{'ID Res':<8} | {'Nama':<15} | {'Lapangan':<10} | {'Jam':<6}")
        print("-" * 50)
        for res in daftar_res:
            if nama_cari in res['nama_penyewa'].lower():
                print(f"{res['id_reservasi']:<8} | {res['nama_penyewa']:<15} | {res['id_lapangan']:<10} | {res['jam']:<6}")
                ditemukan = True
                
        if not ditemukan:
            print("Data reservasi tidak ditemukan.")

    # --- IMPLEMENTASI ALGORITMA SORTING (Bubble Sort) ---
    def lihat_riwayat_urut(self):
        print("\n=== RIWAYAT RESERVASI (TERURUT NAMA) ===")
        ll = self.load_reservasi_to_linked_list()
        daftar_res = ll.to_list()
        
        n = len(daftar_res)
        for i in range(n):
            for j in range(0, n-i-1):
                if daftar_res[j]['nama_penyewa'].lower() > daftar_res[j+1]['nama_penyewa'].lower():
                    daftar_res[j], daftar_res[j+1] = daftar_res[j+1], daftar_res[j]
                    
        print(f"\n{'ID Res':<8} | {'Nama':<15} | {'Lapangan':<10} | {'Jam':<6} | {'Total':<8}")
        print("-" * 55)
        for res in daftar_res:
            print(f"{res['id_reservasi']:<8} | {res['nama_penyewa']:<15} | {res['id_lapangan']:<10} | {res['jam']:<6} | {res['total_bayar']:<8}")

    # --- U / UPDATE: Mengubah Nama Penyewa ---
    def update_reservasi(self):
        print("\n=== UPDATE NAMA PENYEWA ===")
        id_cari = input("Masukkan ID Reservasi yang ingin diubah: ").upper()
        
        data_reservasi = []
        ditemukan = False
        
        with open(self.file_reservasi, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['id_reservasi'] == id_cari:
                    nama_baru = input(f"Masukkan nama baru (Sebelumnya: {row['nama_penyewa']}): ")
                    row['nama_penyewa'] = nama_baru
                    ditemukan = True
                data_reservasi.append(row)
                
        if ditemukan:
            with open(self.file_reservasi, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id_reservasi', 'nama_penyewa', 'id_lapangan', 'jam', 'total_bayar'])
                writer.writeheader()
                writer.writerows(data_reservasi)
            print("✓ Data reservasi berhasil diperbarui!")
        else:
            print("ID Reservasi tidak ditemukan.")

    # --- D / DELETE: Membatalakan/Menghapus Reservasi ---
    def batalkan_reservasi(self):
        print("\n=== PEMBATALAN (DELETE) RESERVASI ===")
        id_cari = input("Masukkan ID Reservasi yang ingin dibatalkan: ").upper()
        
        data_reservasi = []
        target_lapangan = None
        target_jam = None
        ditemukan = False
        
        with open(self.file_reservasi, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['id_reservasi'] == id_cari:
                    target_lapangan = row['id_lapangan']
                    target_jam = row['jam']
                    ditemukan = True
                    continue
                data_reservasi.append(row)
                
        if not ditemukan:
            print("ID Reservasi tidak ditemukan.")
            return

        with open(self.file_reservasi, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id_reservasi', 'nama_penyewa', 'id_lapangan', 'jam', 'total_bayar'])
            writer.writeheader()
            writer.writerows(data_reservasi)
            
        data_lapangan = []
        with open(self.file_lapangan, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['id_lapangan'] == target_lapangan and row['jam'] == target_jam:
                    row['status'] = 'Kosong'
                data_lapangan.append(row)
                
        with open(self.file_lapangan, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id_lapangan', 'nama_lapangan', 'jam', 'status'])
            writer.writeheader()
            writer.writerows(data_lapangan)
            
        print("✓ Reservasi berhasil dibatalkan!")

# ==========================================
# 3. MENU UTAMA INTERFAZ COMMAND LINE (CLI)
# ==========================================
def main():
    sistem = SistemFutsal()
    while True:
        print("\n=======================================")
        print("    SISTEM MANAJEMEN RESERVASI FUTSAL  ")
        print("=======================================")
        print("1. Lihat Ketersediaan Lapangan (Read)")
        print("2. Booking Lapangan Baru (Create)")
        print("3. Cari Reservasi Nama (Searching)")
        print("4. Urutkan Riwayat Booking (Sorting)")
        print("5. Ubah Nama Penyewa (Update)")
        print("6. Batalkan Booking Lapangan (Delete)")
        print("7. Keluar Aplikasi")
        pilihan = input("Pilih menu (1-7): ")

        if pilihan == '1':
            sistem.lihat_lapangan()
        elif pilihan == '2':
            sistem.buat_reservasi()
        elif pilihan == '3':
            sistem.cari_reservasi()
        elif pilihan == '4':
            sistem.lihat_riwayat_urut()
        elif pilihan == '5':
            sistem.update_reservasi()
        elif pilihan == '6':
            sistem.batalkan_reservasi()
        elif pilihan == '7':
            print("Terima kasih telah menggunakan sistem!")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()