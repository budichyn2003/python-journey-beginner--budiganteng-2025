import re

class Member:
    def __init__(self, id, name, email, phone):
        self._id = id
        self._name = name
        self._email = email
        self._phone = phone
        self._borrowed_books = []  # List ID buku yang dipinjam
        self._validate()

    def _validate(self):
        """Memvalidasi data anggota"""
        if not self._name:
            raise ValueError("Nama tidak boleh kosong!")
        
        # Validasi format email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self._email):
            raise ValueError("Format email tidak valid!")
        
        # Validasi nomor telepon (minimal 10 digit, hanya angka)
        phone_pattern = r'^\d{10,}$'
        if not re.match(phone_pattern, self._phone):
            raise ValueError("Nomor telepon tidak valid (minimal 10 digit)!")

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Nama tidak boleh kosong!")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise ValueError("Format email tidak valid!")
        self._email = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        phone_pattern = r'^\d{10,}$'
        if not re.match(phone_pattern, value):
            raise ValueError("Nomor telepon tidak valid (minimal 10 digit)!")
        self._phone = value

    @property
    def borrowed_books(self):
        return self._borrowed_books.copy()

    def can_borrow(self):
        """Mengecek apakah anggota masih bisa meminjam buku"""
        return len(self._borrowed_books) < 3

    def borrow_book(self, book_id):
        """Menambahkan buku ke daftar pinjaman"""
        if not self.can_borrow():
            raise ValueError("Sudah mencapai batas maksimal peminjaman (3 buku)!")
        if book_id in self._borrowed_books:
            raise ValueError("Buku ini sudah dipinjam!")
        self._borrowed_books.append(book_id)
        return True

    def return_book(self, book_id):
        """Menghapus buku dari daftar pinjaman"""
        if book_id not in self._borrowed_books:
            raise ValueError("Buku ini tidak sedang dipinjam!")
        self._borrowed_books.remove(book_id)
        return True

    def to_dict(self):
        """Mengkonversi objek ke dictionary"""
        return {
            'id': self._id,
            'name': self._name,
            'email': self._email,
            'phone': self._phone,
            'borrowed_books': self._borrowed_books
        }

    @classmethod
    def from_dict(cls, data):
        """Membuat objek dari dictionary"""
        member = cls(
            id=data['id'],
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )
        member._borrowed_books = data.get('borrowed_books', [])
        return member

    def __str__(self):
        borrowed = len(self._borrowed_books)
        return f"{self._name} ({self._email}) - {borrowed} buku dipinjam"