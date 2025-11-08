import json
import os
from datetime import datetime, date

class TodoManager:
    def __init__(self, file_path="tasks.json"):
        """Inisialisasi TodoManager"""
        self.file_path = file_path
        self.categories = ["Pekerjaan", "Pribadi", "Belanja", "Belajar", "Lainnya"]
        self.priorities = ["Tinggi", "Sedang", "Rendah"]
        self.statuses = ["Pending", "In Progress", "Completed", "Cancelled"]
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Memuat tugas dari file JSON"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_tasks(self):
        """Menyimpan tugas ke file JSON"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=4, ensure_ascii=False)

    def generate_task_id(self):
        """Generate ID unik untuk tugas baru"""
        if not self.tasks:
            return "task_001"
        last_id = max([int(task['id'].split('_')[1]) for task in self.tasks])
        return f"task_{last_id + 1:03d}"

    def add_task(self, title, description, category, priority, due_date):
        """Menambahkan tugas baru"""
        if category not in self.categories:
            raise ValueError("Kategori tidak valid!")
        if priority not in self.priorities:
            raise ValueError("Prioritas tidak valid!")

        # Validasi format tanggal
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Format tanggal tidak valid! Gunakan YYYY-MM-DD")

        task = {
            "id": self.generate_task_id(),
            "title": title,
            "description": description,
            "category": category,
            "priority": priority,
            "status": "Pending",
            "due_date": due_date,
            "created_at": date.today().isoformat(),
            "completed_at": None,
            "progress": 0
        }

        self.tasks.append(task)
        self.save_tasks()
        return task

    def get_all_tasks(self):
        """Mengambil semua tugas"""
        return sorted(self.tasks, key=lambda x: (
            self.priorities.index(x['priority']),
            x['due_date']
        ))

    def get_task_by_id(self, task_id):
        """Mengambil tugas berdasarkan ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None

    def get_tasks_by_status(self, status):
        """Mengambil tugas berdasarkan status"""
        if status not in self.statuses:
            raise ValueError("Status tidak valid!")
        return [task for task in self.tasks if task['status'] == status]

    def get_tasks_by_priority(self, priority):
        """Mengambil tugas berdasarkan prioritas"""
        if priority not in self.priorities:
            raise ValueError("Prioritas tidak valid!")
        return [task for task in self.tasks if task['priority'] == priority]

    def get_tasks_by_category(self, category):
        """Mengambil tugas berdasarkan kategori"""
        if category not in self.categories:
            raise ValueError("Kategori tidak valid!")
        return [task for task in self.tasks if task['category'] == category]

    def update_task_status(self, task_id, new_status):
        """Mengupdate status tugas"""
        if new_status not in self.statuses:
            raise ValueError("Status tidak valid!")

        task = self.get_task_by_id(task_id)
        if not task:
            raise ValueError("Tugas tidak ditemukan!")

        task['status'] = new_status
        if new_status == "Completed":
            task['completed_at'] = date.today().isoformat()
            task['progress'] = 100
        elif new_status == "Cancelled":
            task['completed_at'] = date.today().isoformat()
        else:
            task['completed_at'] = None

        self.save_tasks()
        return task

    def update_task_progress(self, task_id, progress):
        """Mengupdate progress tugas"""
        if not 0 <= progress <= 100:
            raise ValueError("Progress harus antara 0-100!")

        task = self.get_task_by_id(task_id)
        if not task:
            raise ValueError("Tugas tidak ditemukan!")

        task['progress'] = progress
        if progress == 100:
            task['status'] = "Completed"
            task['completed_at'] = date.today().isoformat()
        elif progress == 0:
            task['status'] = "Pending"
            task['completed_at'] = None
        else:
            task['status'] = "In Progress"
            task['completed_at'] = None

        self.save_tasks()
        return task

    def update_task_details(self, task_id, title=None, description=None, 
                          category=None, priority=None, due_date=None):
        """Mengupdate detail tugas"""
        task = self.get_task_by_id(task_id)
        if not task:
            raise ValueError("Tugas tidak ditemukan!")

        if category and category not in self.categories:
            raise ValueError("Kategori tidak valid!")
        if priority and priority not in self.priorities:
            raise ValueError("Prioritas tidak valid!")
        if due_date:
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Format tanggal tidak valid! Gunakan YYYY-MM-DD")

        if title:
            task['title'] = title
        if description:
            task['description'] = description
        if category:
            task['category'] = category
        if priority:
            task['priority'] = priority
        if due_date:
            task['due_date'] = due_date

        self.save_tasks()
        return task

    def delete_task(self, task_id):
        """Menghapus tugas"""
        task = self.get_task_by_id(task_id)
        if not task:
            raise ValueError("Tugas tidak ditemukan!")

        self.tasks.remove(task)
        self.save_tasks()
        return True

    def delete_completed_tasks(self):
        """Menghapus semua tugas yang sudah selesai"""
        initial_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if task['status'] != "Completed"]
        self.save_tasks()
        return initial_count - len(self.tasks)

    def get_overdue_tasks(self):
        """Mengambil tugas yang sudah melewati deadline"""
        today = date.today().isoformat()
        return [
            task for task in self.tasks
            if task['due_date'] < today and task['status'] not in ["Completed", "Cancelled"]
        ]