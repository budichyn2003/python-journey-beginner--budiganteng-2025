import unittest
import os
import json
from datetime import date, timedelta
from todo_manager import TodoManager

class TestTodoManager(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.test_file = "test_tasks.json"
        self.manager = TodoManager(self.test_file)

    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_task(self):
        """Test adding a new task"""
        task = self.manager.add_task(
            "Test Task",
            "Test Description",
            "Pekerjaan",
            "Tinggi",
            "2025-12-31"
        )
        
        self.assertIsNotNone(task)
        self.assertTrue(task['id'].startswith('task_'))
        self.assertEqual(task['title'], "Test Task")
        self.assertEqual(task['status'], "Pending")
        self.assertEqual(task['progress'], 0)

    def test_invalid_category(self):
        """Test adding task with invalid category"""
        with self.assertRaises(ValueError):
            self.manager.add_task(
                "Test Task",
                "Test Description",
                "Invalid",
                "Tinggi",
                "2025-12-31"
            )

    def test_invalid_priority(self):
        """Test adding task with invalid priority"""
        with self.assertRaises(ValueError):
            self.manager.add_task(
                "Test Task",
                "Test Description",
                "Pekerjaan",
                "Invalid",
                "2025-12-31"
            )

    def test_invalid_date(self):
        """Test adding task with invalid date"""
        with self.assertRaises(ValueError):
            self.manager.add_task(
                "Test Task",
                "Test Description",
                "Pekerjaan",
                "Tinggi",
                "invalid-date"
            )

    def test_get_tasks_by_status(self):
        """Test filtering tasks by status"""
        self.manager.add_task(
            "Task 1", "Desc 1", "Pekerjaan", "Tinggi", "2025-12-31"
        )
        self.manager.add_task(
            "Task 2", "Desc 2", "Pribadi", "Sedang", "2025-12-31"
        )

        # Update status of second task to completed
        self.manager.update_task_status(
            self.manager.tasks[1]['id'], 
            "Completed"
        )

        pending_tasks = self.manager.get_tasks_by_status("Pending")
        completed_tasks = self.manager.get_tasks_by_status("Completed")

        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(pending_tasks[0]['title'], "Task 1")
        self.assertEqual(completed_tasks[0]['title'], "Task 2")

    def test_update_task_progress(self):
        """Test updating task progress"""
        task = self.manager.add_task(
            "Test Task",
            "Test Description",
            "Pekerjaan",
            "Tinggi",
            "2025-12-31"
        )

        # Test invalid progress
        with self.assertRaises(ValueError):
            self.manager.update_task_progress(task['id'], 101)
        with self.assertRaises(ValueError):
            self.manager.update_task_progress(task['id'], -1)

        # Test valid progress updates
        updated_task = self.manager.update_task_progress(task['id'], 50)
        self.assertEqual(updated_task['progress'], 50)
        self.assertEqual(updated_task['status'], "In Progress")

        updated_task = self.manager.update_task_progress(task['id'], 100)
        self.assertEqual(updated_task['progress'], 100)
        self.assertEqual(updated_task['status'], "Completed")
        self.assertIsNotNone(updated_task['completed_at'])

    def test_delete_completed_tasks(self):
        """Test deleting completed tasks"""
        # Add three tasks
        self.manager.add_task(
            "Task 1", "Desc 1", "Pekerjaan", "Tinggi", "2025-12-31"
        )
        self.manager.add_task(
            "Task 2", "Desc 2", "Pribadi", "Sedang", "2025-12-31"
        )
        self.manager.add_task(
            "Task 3", "Desc 3", "Belajar", "Rendah", "2025-12-31"
        )

        # Mark two tasks as completed
        self.manager.update_task_status(self.manager.tasks[0]['id'], "Completed")
        self.manager.update_task_status(self.manager.tasks[1]['id'], "Completed")

        # Delete completed tasks
        deleted_count = self.manager.delete_completed_tasks()
        
        self.assertEqual(deleted_count, 2)
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0]['title'], "Task 3")

    def test_get_overdue_tasks(self):
        """Test getting overdue tasks"""
        # Add task with yesterday's date
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        self.manager.add_task(
            "Overdue Task",
            "This task is overdue",
            "Pekerjaan",
            "Tinggi",
            yesterday
        )

        # Add task with future date
        future = (date.today() + timedelta(days=7)).isoformat()
        self.manager.add_task(
            "Future Task",
            "This task is not due yet",
            "Pekerjaan",
            "Tinggi",
            future
        )

        overdue_tasks = self.manager.get_overdue_tasks()
        self.assertEqual(len(overdue_tasks), 1)
        self.assertEqual(overdue_tasks[0]['title'], "Overdue Task")

    def test_task_persistence(self):
        """Test that tasks are properly saved and loaded"""
        # Add a task
        original_task = self.manager.add_task(
            "Persistent Task",
            "This task should persist",
            "Pekerjaan",
            "Tinggi",
            "2025-12-31"
        )

        # Create new manager instance (should load from file)
        new_manager = TodoManager(self.test_file)
        loaded_tasks = new_manager.get_all_tasks()

        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0]['id'], original_task['id'])
        self.assertEqual(loaded_tasks[0]['title'], original_task['title'])

    def test_update_task_details(self):
        """Test updating task details"""
        task = self.manager.add_task(
            "Original Title",
            "Original Description",
            "Pekerjaan",
            "Tinggi",
            "2025-12-31"
        )

        updated_task = self.manager.update_task_details(
            task['id'],
            title="New Title",
            description="New Description",
            category="Pribadi",
            priority="Sedang",
            due_date="2025-12-25"
        )

        self.assertEqual(updated_task['title'], "New Title")
        self.assertEqual(updated_task['description'], "New Description")
        self.assertEqual(updated_task['category'], "Pribadi")
        self.assertEqual(updated_task['priority'], "Sedang")
        self.assertEqual(updated_task['due_date'], "2025-12-25")

if __name__ == '__main__':
    unittest.main()