import unittest
import os
import shutil
import json
from datetime import datetime
from notes_manager import NotesManager

class TestNotesManager(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.test_notes_dir = "test_notes"
        self.test_backup_dir = "test_backup"
        self.manager = NotesManager(self.test_notes_dir, self.test_backup_dir)

    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_notes_dir):
            shutil.rmtree(self.test_notes_dir)
        if os.path.exists(self.test_backup_dir):
            shutil.rmtree(self.test_backup_dir)

    def test_create_note(self):
        """Test creating a new note"""
        note = self.manager.create_note(
            "Test Note",
            "Personal",
            "This is a test note"
        )
        
        self.assertIsNotNone(note)
        self.assertTrue(note['id'].startswith('note_'))
        self.assertEqual(note['title'], "Test Note")
        self.assertEqual(note['category'], "Personal")
        self.assertEqual(note['content'], "This is a test note")

        # Verify file was created
        self.assertTrue(os.path.exists(
            os.path.join(self.test_notes_dir, f"{note['id']}.json")
        ))

    def test_invalid_category(self):
        """Test creating note with invalid category"""
        with self.assertRaises(ValueError):
            self.manager.create_note(
                "Test Note",
                "InvalidCategory",
                "This is a test note"
            )

    def test_get_all_notes(self):
        """Test retrieving all notes"""
        # Create multiple notes
        note1 = self.manager.create_note("Note 1", "Personal", "Content 1")
        note2 = self.manager.create_note("Note 2", "Pekerjaan", "Content 2")
        
        notes = self.manager.get_all_notes()
        self.assertEqual(len(notes), 2)
        self.assertIn(note1['id'], [n['id'] for n in notes])
        self.assertIn(note2['id'], [n['id'] for n in notes])

    def test_search_notes(self):
        """Test searching notes"""
        self.manager.create_note(
            "Meeting Notes",
            "Pekerjaan",
            "Discussion about project timeline"
        )
        self.manager.create_note(
            "Shopping List",
            "Personal",
            "Buy groceries"
        )

        # Search by title
        results = self.manager.search_notes("meeting")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Meeting Notes")

        # Search by content
        results = self.manager.search_notes("groceries")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Shopping List")

    def test_update_note(self):
        """Test updating a note"""
        note = self.manager.create_note(
            "Original Title",
            "Personal",
            "Original content"
        )

        updated = self.manager.update_note(
            note['id'],
            title="Updated Title",
            content="Updated content"
        )

        self.assertEqual(updated['title'], "Updated Title")
        self.assertEqual(updated['content'], "Updated content")
        self.assertEqual(updated['category'], "Personal")

    def test_delete_note(self):
        """Test deleting a note"""
        note = self.manager.create_note(
            "To Delete",
            "Personal",
            "This note will be deleted"
        )

        # Verify note exists
        self.assertTrue(os.path.exists(
            os.path.join(self.test_notes_dir, f"{note['id']}.json")
        ))

        # Delete note
        self.assertTrue(self.manager.delete_note(note['id']))

        # Verify note was deleted
        self.assertFalse(os.path.exists(
            os.path.join(self.test_notes_dir, f"{note['id']}.json")
        ))

    def test_backup_restore(self):
        """Test backup and restore functionality"""
        # Create some notes
        self.manager.create_note("Note 1", "Personal", "Content 1")
        self.manager.create_note("Note 2", "Pekerjaan", "Content 2")

        # Create backup
        backup_file = self.manager.create_backup()
        self.assertIsNotNone(backup_file)
        self.assertTrue(os.path.exists(backup_file))

        # Delete all notes
        shutil.rmtree(self.test_notes_dir)
        os.makedirs(self.test_notes_dir)

        # Restore from backup
        self.assertTrue(self.manager.restore_backup(backup_file))

        # Verify notes were restored
        notes = self.manager.get_all_notes()
        self.assertEqual(len(notes), 2)

    def test_get_notes_by_date(self):
        """Test retrieving notes by date"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        note = self.manager.create_note(
            "Today's Note",
            "Personal",
            "Created today"
        )

        notes = self.manager.get_notes_by_date(today)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]['id'], note['id'])

    def test_get_notes_by_category(self):
        """Test retrieving notes by category"""
        self.manager.create_note("Note 1", "Personal", "Personal content")
        self.manager.create_note("Note 2", "Pekerjaan", "Work content")
        self.manager.create_note("Note 3", "Personal", "More personal content")

        personal_notes = self.manager.get_notes_by_category("Personal")
        work_notes = self.manager.get_notes_by_category("Pekerjaan")

        self.assertEqual(len(personal_notes), 2)
        self.assertEqual(len(work_notes), 1)

if __name__ == '__main__':
    unittest.main()