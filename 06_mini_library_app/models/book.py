import re
from datetime import datetime

class Book:
    def __init__(self, id, title, author, year, quantity):
        self._id = id
        self._title = title
        self._author = author
        self._year = year
        self._quantity = quantity
        self._validate()

    def _validate(self):
        """Memvalidasi data buku"""
        if not self._title or not self._author:
            raise ValueError("Judul dan penulis tidak boleh kosong!")
        
        current_year = datetime.now().year
        if not isinstance(self._year, int) or self._year < 1000 or self._year > current_year:
            raise ValueError(f"Tahun terbit harus antara 1000 dan {current_year}!")
        
        if not isinstance(self._quantity, int) or self._quantity < 0:
            raise ValueError("Jumlah buku tidak valid!")

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Judul tidak boleh kosong!")
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not value:
            raise ValueError("Penulis tidak boleh kosong!")
        self._author = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        current_year = datetime.now().year
        if not isinstance(value, int) or value < 1000 or value > current_year:
            raise ValueError(f"Tahun terbit harus antara 1000 dan {current_year}!")
        self._year = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Jumlah buku tidak valid!")
        self._quantity = value

    def is_available(self):
        """Mengecek ketersediaan buku"""
        return self._quantity > 0

    def borrow(self):
        """Meminjam satu buku"""
        if not self.is_available():
            raise ValueError("Buku tidak tersedia!")
        self._quantity -= 1
        return True

    def return_book(self):
        """Mengembalikan satu buku"""
        self._quantity += 1
        return True

    def to_dict(self):
        """Mengkonversi objek ke dictionary"""
        return {
            'id': self._id,
            'title': self._title,
            'author': self._author,
            'year': self._year,
            'quantity': self._quantity
        }

    @classmethod
    def from_dict(cls, data):
        """Membuat objek dari dictionary"""
        return cls(
            id=data['id'],
            title=data['title'],
            author=data['author'],
            year=data['year'],
            quantity=data['quantity']
        )

    def __str__(self):
        return f"{self._title} by {self._author} ({self._year}) - {self._quantity} tersedia"