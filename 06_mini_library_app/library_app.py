import json
import os
from datetime import datetime
from models.book import Book
from models.member import Member
from models.borrowing import Borrowing

class LibraryApp:
    def __init__(self, data_dir="data"):
        """Inisialisasi Library App"""
        self.data_dir = data_dir
        self.books_file = os.path.join(data_dir, "books.json")
        self.members_file = os.path.join(data_dir, "members.json")
        self.borrowings_file = os.path.join(data_dir, "borrowings.json")
        
        # Buat direktori jika belum ada
        os.makedirs(data_dir, exist_ok=True)
        
        # Load data
        self.books = self.load_books()
        self.members = self.load_members()
        self.borrowings = self.load_borrowings()

    def load_books(self):
        """Memuat data buku dari file"""
        if os.path.exists(self.books_file):
            with open(self.books_file, 'r') as f:
                data = json.load(f)
                return [Book.from_dict(book_data) for book_data in data]
        return []

    def save_books(self):
        """Menyimpan data buku ke file"""
        with open(self.books_file, 'w') as f:
            data = [book.to_dict() for book in self.books]
            json.dump(data, f, indent=4)

    def load_members(self):
        """Memuat data anggota dari file"""
        if os.path.exists(self.members_file):
            with open(self.members_file, 'r') as f:
                data = json.load(f)
                return [Member.from_dict(member_data) for member_data in data]
        return []

    def save_members(self):
        """Menyimpan data anggota ke file"""
        with open(self.members_file, 'w') as f:
            data = [member.to_dict() for member in self.members]
            json.dump(data, f, indent=4)

    def load_borrowings(self):
        """Memuat data peminjaman dari file"""
        if os.path.exists(self.borrowings_file):
            with open(self.borrowings_file, 'r') as f:
                data = json.load(f)
                return [Borrowing.from_dict(borrow_data) for borrow_data in data]
        return []

    def save_borrowings(self):
        """Menyimpan data peminjaman ke file"""
        with open(self.borrowings_file, 'w') as f:
            data = [borrowing.to_dict() for borrowing in self.borrowings]
            json.dump(data, f, indent=4)

    def generate_id(self, prefix, items):
        """Generate ID unik"""
        if not items:
            return f"{prefix}_001"
        last_id = max([int(item.id.split('_')[1]) for item in items])
        return f"{prefix}_{last_id + 1:03d}"

    # Book Management
    def add_book(self, title, author, year, quantity):
        """Menambahkan buku baru"""
        book_id = self.generate_id("book", self.books)
        book = Book(book_id, title, author, year, quantity)
        self.books.append(book)
        self.save_books()
        return book

    def get_book(self, book_id):
        """Mencari buku berdasarkan ID"""
        return next((book for book in self.books if book.id == book_id), None)

    def update_book(self, book_id, title=None, author=None, year=None, quantity=None):
        """Mengupdate informasi buku"""
        book = self.get_book(book_id)
        if not book:
            raise ValueError("Buku tidak ditemukan!")

        if title:
            book.title = title
        if author:
            book.author = author
        if year:
            book.year = year
        if quantity is not None:
            book.quantity = quantity

        self.save_books()
        return book

    def delete_book(self, book_id):
        """Menghapus buku"""
        book = self.get_book(book_id)
        if not book:
            raise ValueError("Buku tidak ditemukan!")
        
        # Cek apakah buku sedang dipinjam
        active_borrowings = [b for b in self.borrowings if b.book_id == book_id and not b.is_returned()]
        if active_borrowings:
            raise ValueError("Buku sedang dipinjam dan tidak dapat dihapus!")

        self.books.remove(book)
        self.save_books()
        return True

    def search_books(self, keyword):
        """Mencari buku berdasarkan judul atau penulis"""
        keyword = keyword.lower()
        return [
            book for book in self.books
            if keyword in book.title.lower() or keyword in book.author.lower()
        ]

    # Member Management
    def add_member(self, name, email, phone):
        """Menambahkan anggota baru"""
        member_id = self.generate_id("member", self.members)
        member = Member(member_id, name, email, phone)
        self.members.append(member)
        self.save_members()
        return member

    def get_member(self, member_id):
        """Mencari anggota berdasarkan ID"""
        return next((member for member in self.members if member.id == member_id), None)

    def update_member(self, member_id, name=None, email=None, phone=None):
        """Mengupdate informasi anggota"""
        member = self.get_member(member_id)
        if not member:
            raise ValueError("Anggota tidak ditemukan!")

        if name:
            member.name = name
        if email:
            member.email = email
        if phone:
            member.phone = phone

        self.save_members()
        return member

    def delete_member(self, member_id):
        """Menghapus anggota"""
        member = self.get_member(member_id)
        if not member:
            raise ValueError("Anggota tidak ditemukan!")

        # Cek apakah anggota masih memiliki peminjaman aktif
        active_borrowings = [b for b in self.borrowings if b.member_id == member_id and not b.is_returned()]
        if active_borrowings:
            raise ValueError("Anggota masih memiliki peminjaman aktif!")

        self.members.remove(member)
        self.save_members()
        return True

    def search_members(self, keyword):
        """Mencari anggota berdasarkan nama atau email"""
        keyword = keyword.lower()
        return [
            member for member in self.members
            if keyword in member.name.lower() or keyword in member.email.lower()
        ]

    # Borrowing Management
    def borrow_book(self, member_id, book_id):
        """Proses peminjaman buku"""
        member = self.get_member(member_id)
        if not member:
            raise ValueError("Anggota tidak ditemukan!")

        book = self.get_book(book_id)
        if not book:
            raise ValueError("Buku tidak ditemukan!")

        if not book.is_available():
            raise ValueError("Buku tidak tersedia!")

        if not member.can_borrow():
            raise ValueError("Anggota sudah mencapai batas peminjaman!")

        # Buat peminjaman baru
        borrow_id = self.generate_id("borrow", self.borrowings)
        borrowing = Borrowing(
            borrow_id,
            member_id,
            book_id,
            datetime.now().strftime('%Y-%m-%d')
        )

        # Update status
        book.borrow()
        member.borrow_book(book_id)

        self.borrowings.append(borrowing)
        self.save_all()
        return borrowing

    def return_book(self, borrowing_id):
        """Proses pengembalian buku"""
        borrowing = next((b for b in self.borrowings if b.id == borrowing_id), None)
        if not borrowing:
            raise ValueError("Data peminjaman tidak ditemukan!")

        if borrowing.is_returned():
            raise ValueError("Buku sudah dikembalikan!")

        member = self.get_member(borrowing.member_id)
        book = self.get_book(borrowing.book_id)

        # Update status
        return_date = datetime.now()
        borrowing.return_date = return_date
        book.return_book()
        member.return_book(book.id)

        # Hitung denda
        fine = borrowing.calculate_fine(return_date)

        self.save_all()
        return (borrowing, fine)

    def get_active_borrowings(self, member_id=None):
        """Mendapatkan daftar peminjaman aktif"""
        active = [b for b in self.borrowings if not b.is_returned()]
        if member_id:
            active = [b for b in active if b.member_id == member_id]
        return active

    def get_borrowing_history(self, member_id=None):
        """Mendapatkan riwayat peminjaman"""
        history = self.borrowings
        if member_id:
            history = [b for b in history if b.member_id == member_id]
        return sorted(history, key=lambda x: x.borrow_date, reverse=True)

    def check_overdue_books(self):
        """Mengecek buku-buku yang terlambat dikembalikan"""
        today = datetime.now()
        return [
            (b, self.get_member(b.member_id), self.get_book(b.book_id))
            for b in self.borrowings
            if not b.is_returned() and b.calculate_fine(today) > 0
        ]

    def save_all(self):
        """Menyimpan semua data"""
        self.save_books()
        self.save_members()
        self.save_borrowings()

    def get_statistics(self):
        """Mendapatkan statistik perpustakaan"""
        return {
            'total_books': sum(book.quantity for book in self.books),
            'unique_books': len(self.books),
            'total_members': len(self.members),
            'active_borrowings': len(self.get_active_borrowings()),
            'total_borrowings': len(self.borrowings)
        }
if __name__ == "__main__":
    app = LibraryApp()
    
    while True:
        print("\n" + "="*40)
        print("📚 MINI LIBRARY APP")
        print("="*40)
        print("1. Lihat Buku")
        print("2. Tambah Buku")
        print("3. Lihat Anggota") 
        print("4. Tambah Anggota")
        print("5. Statistik")
        print("6. Keluar")
        print("="*40)
        
        pilihan = input("Pilih menu (1-6): ")
        
        if pilihan == '1':
            print("\n📚 DAFTAR BUKU")
            if not app.books:
                print("Tidak ada buku")
            else:
                for book in app.books:
                    print(f"- {book.id}: {book.title} oleh {book.author} ({book.year}) - Stok: {book.quantity}")
                    
        elif pilihan == '2':
            print("\n➕ TAMBAH BUKU")
            judul = input("Judul: ")
            penulis = input("Penulis: ")
            tahun = int(input("Tahun: "))
            stok = int(input("Stok: "))
            buku = app.add_book(judul, penulis, tahun, stok)
            print(f"✅ Berhasil menambahkan: {buku.title}")
            
        elif pilihan == '3':
            print("\n👥 DAFTAR ANGGOTA")
            if not app.members:
                print("Tidak ada anggota")
            else:
                for member in app.members:
                    print(f"- {member.id}: {member.name} - {member.email}")
                    
        elif pilihan == '4':
            print("\n➕ TAMBAH ANGGOTA")
            nama = input("Nama: ")
            email = input("Email: ")
            
            # Validasi telepon
            while True:
                telepon = input("Telepon (minimal 10 digit): ")
                if len(telepon) >= 10 and telepon.isdigit():
                    break
                else:
                    print("❌ Nomor telepon harus minimal 10 digit angka!")
            
            try:
                anggota = app.add_member(nama, email, telepon)
                print(f"✅ Berhasil menambahkan: {anggota.name}")
            except ValueError as e:
                print(f"❌ Error: {e}")
            
        elif pilihan == '5':
            stats = app.get_statistics()
            print("\n📊 STATISTIK")
            print(f"Total Buku: {stats['total_books']}")
            print(f"Judul Unik: {stats['unique_books']}") 
            print(f"Total Anggota: {stats['total_members']}")
            print(f"Peminjaman Aktif: {stats['active_borrowings']}")
            
        elif pilihan == '6':
            print("👋 Terima kasih!")
            break
            
        else:
            print("❌ Pilihan tidak valid!")