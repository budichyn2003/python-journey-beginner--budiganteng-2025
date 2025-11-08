import unittest
import os
import json
from datetime import datetime, timedelta
from models.book import Book
from models.member import Member
from models.borrowing import Borrowing
from library_app import LibraryApp

class TestLibraryApp(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.test_data_dir = "test_data"
        self.app = LibraryApp(self.test_data_dir)

    def tearDown(self):
        """Clean up test environment"""
        for file in ['books.json', 'members.json', 'borrowings.json']:
            path = os.path.join(self.test_data_dir, file)
            if os.path.exists(path):
                os.remove(path)
        if os.path.exists(self.test_data_dir):
            os.rmdir(self.test_data_dir)

    def test_add_book(self):
        """Test adding a new book"""
        book = self.app.add_book("Test Book", "Test Author", 2025, 5)
        self.assertIsInstance(book, Book)
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(len(self.app.books), 1)

    def test_add_invalid_book(self):
        """Test adding a book with invalid data"""
        with self.assertRaises(ValueError):
            self.app.add_book("", "Test Author", 2025, 5)  # Empty title
        with self.assertRaises(ValueError):
            self.app.add_book("Test Book", "", 2025, 5)    # Empty author
        with self.assertRaises(ValueError):
            self.app.add_book("Test Book", "Test Author", 3000, 5)  # Invalid year

    def test_add_member(self):
        """Test adding a new member"""
        member = self.app.add_member(
            "Test User",
            "test@email.com",
            "1234567890"
        )
        self.assertIsInstance(member, Member)
        self.assertEqual(member.name, "Test User")
        self.assertEqual(len(self.app.members), 1)

    def test_add_invalid_member(self):
        """Test adding a member with invalid data"""
        with self.assertRaises(ValueError):
            self.app.add_member("", "test@email.com", "1234567890")  # Empty name
        with self.assertRaises(ValueError):
            self.app.add_member("Test User", "invalid-email", "1234567890")  # Invalid email
        with self.assertRaises(ValueError):
            self.app.add_member("Test User", "test@email.com", "123")  # Invalid phone

    def test_borrow_book(self):
        """Test borrowing a book"""
        # Add book and member
        book = self.app.add_book("Test Book", "Test Author", 2025, 1)
        member = self.app.add_member("Test User", "test@email.com", "1234567890")

        # Borrow book
        borrowing = self.app.borrow_book(member.id, book.id)
        self.assertIsInstance(borrowing, Borrowing)
        self.assertEqual(book.quantity, 0)
        self.assertEqual(len(member.borrowed_books), 1)

    def test_invalid_borrow(self):
        """Test invalid borrowing scenarios"""
        book = self.app.add_book("Test Book", "Test Author", 2025, 1)
        member = self.app.add_member("Test User", "test@email.com", "1234567890")

        # Borrow the only copy
        self.app.borrow_book(member.id, book.id)

        # Try to borrow unavailable book
        with self.assertRaises(ValueError):
            self.app.borrow_book(member.id, book.id)

        # Add more books and try to exceed borrow limit
        self.app.add_book("Book 2", "Author 2", 2025, 1)
        self.app.add_book("Book 3", "Author 3", 2025, 1)
        self.app.add_book("Book 4", "Author 4", 2025, 1)

        self.app.borrow_book(member.id, "book_002")
        self.app.borrow_book(member.id, "book_003")

        # Try to borrow fourth book
        with self.assertRaises(ValueError):
            self.app.borrow_book(member.id, "book_004")

    def test_return_book(self):
        """Test returning a book"""
        book = self.app.add_book("Test Book", "Test Author", 2025, 1)
        member = self.app.add_member("Test User", "test@email.com", "1234567890")

        # Borrow and return book
        borrowing = self.app.borrow_book(member.id, book.id)
        returned, fine = self.app.return_book(borrowing.id)

        self.assertTrue(returned.is_returned())
        self.assertEqual(book.quantity, 1)
        self.assertEqual(len(member.borrowed_books), 0)

    def test_overdue_books(self):
        """Test overdue book detection"""
        book = self.app.add_book("Test Book", "Test Author", 2025, 1)
        member = self.app.add_member("Test User", "test@email.com", "1234567890")

        # Simulate borrowing 15 days ago
        borrowing = self.app.borrow_book(member.id, book.id)
        past_date = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
        borrowing._borrow_date = past_date

        overdue = self.app.check_overdue_books()
        self.assertEqual(len(overdue), 1)
        self.assertEqual(overdue[0][0].id, borrowing.id)

    def test_search_books(self):
        """Test book search functionality"""
        self.app.add_book("Python Programming", "John Doe", 2025, 1)
        self.app.add_book("Java Basics", "Jane Smith", 2025, 1)
        self.app.add_book("Python for Beginners", "Bob Wilson", 2025, 1)

        results = self.app.search_books("Python")
        self.assertEqual(len(results), 2)
        
        results = self.app.search_books("Java")
        self.assertEqual(len(results), 1)

    def test_search_members(self):
        """Test member search functionality"""
        self.app.add_member("John Doe", "john@email.com", "1234567890")
        self.app.add_member("Jane Doe", "jane@email.com", "1234567891")
        self.app.add_member("Bob Wilson", "bob@email.com", "1234567892")

        results = self.app.search_members("Doe")
        self.assertEqual(len(results), 2)
        
        results = self.app.search_members("bob@email.com")
        self.assertEqual(len(results), 1)

    def test_statistics(self):
        """Test library statistics"""
        # Add books and members
        self.app.add_book("Book 1", "Author 1", 2025, 3)
        self.app.add_book("Book 2", "Author 2", 2025, 2)
        self.app.add_member("User 1", "user1@email.com", "1234567890")
        self.app.add_member("User 2", "user2@email.com", "1234567891")

        # Create some borrowings
        self.app.borrow_book("member_001", "book_001")
        self.app.borrow_book("member_002", "book_002")

        stats = self.app.get_statistics()
        self.assertEqual(stats['total_books'], 5)  # 3 + 2
        self.assertEqual(stats['unique_books'], 2)
        self.assertEqual(stats['total_members'], 2)
        self.assertEqual(stats['active_borrowings'], 2)
        self.assertEqual(stats['total_borrowings'], 2)

if __name__ == '__main__':
    unittest.main()