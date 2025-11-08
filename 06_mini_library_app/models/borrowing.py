from datetime import datetime, timedelta

class Borrowing:
    def __init__(self, id, member_id, book_id, borrow_date):
        self._id = id
        self._member_id = member_id
        self._book_id = book_id
        self._borrow_date = borrow_date
        self._return_date = None
        self._validate()

    def _validate(self):
        """Memvalidasi data peminjaman"""
        if not all([self._id, self._member_id, self._book_id, self._borrow_date]):
            raise ValueError("Semua data peminjaman harus diisi!")
        
        try:
            if isinstance(self._borrow_date, str):
                datetime.strptime(self._borrow_date, '%Y-%m-%d')
            elif not isinstance(self._borrow_date, datetime):
                raise ValueError()
        except ValueError:
            raise ValueError("Format tanggal pinjam tidak valid!")

    @property
    def id(self):
        return self._id

    @property
    def member_id(self):
        return self._member_id

    @property
    def book_id(self):
        return self._book_id

    @property
    def borrow_date(self):
        return self._borrow_date

    @property
    def return_date(self):
        return self._return_date

    @return_date.setter
    def return_date(self, value):
        """Set tanggal pengembalian"""
        if value:
            try:
                if isinstance(value, str):
                    datetime.strptime(value, '%Y-%m-%d')
                elif not isinstance(value, datetime):
                    raise ValueError()
            except ValueError:
                raise ValueError("Format tanggal kembali tidak valid!")
        self._return_date = value

    def is_returned(self):
        """Mengecek apakah buku sudah dikembalikan"""
        return self._return_date is not None

    def calculate_fine(self, return_date=None):
        """Menghitung denda keterlambatan"""
        if not return_date:
            return_date = datetime.now()
        elif isinstance(return_date, str):
            return_date = datetime.strptime(return_date, '%Y-%m-%d')

        if isinstance(self._borrow_date, str):
            borrow_date = datetime.strptime(self._borrow_date, '%Y-%m-%d')
        else:
            borrow_date = self._borrow_date

        # Durasi peminjaman maksimal 14 hari
        due_date = borrow_date + timedelta(days=14)
        
        if return_date <= due_date:
            return 0
        
        # Denda Rp 1.000 per hari keterlambatan
        days_late = (return_date - due_date).days
        return days_late * 1000

    def to_dict(self):
        """Mengkonversi objek ke dictionary"""
        return {
            'id': self._id,
            'member_id': self._member_id,
            'book_id': self._book_id,
            'borrow_date': self._borrow_date.isoformat() if isinstance(self._borrow_date, datetime)
                         else self._borrow_date,
            'return_date': self._return_date.isoformat() if self._return_date and 
                         isinstance(self._return_date, datetime) else self._return_date
        }

    @classmethod
    def from_dict(cls, data):
        """Membuat objek dari dictionary"""
        borrowing = cls(
            id=data['id'],
            member_id=data['member_id'],
            book_id=data['book_id'],
            borrow_date=data['borrow_date']
        )
        borrowing.return_date = data.get('return_date')
        return borrowing

    def __str__(self):
        status = "Dikembalikan" if self.is_returned() else "Dipinjam"
        return f"Peminjaman {self._id}: Buku {self._book_id} oleh {self._member_id} - {status}"