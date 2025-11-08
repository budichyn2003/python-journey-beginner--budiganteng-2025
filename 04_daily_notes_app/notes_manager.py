import json
import os
from datetime import datetime
import shutil

class NotesManager:
    def __init__(self, notes_dir="notes", backup_dir="backup"):
        """Inisialisasi NotesManager"""
        self.notes_dir = notes_dir
        self.backup_dir = backup_dir
        self.categories = ["Personal", "Pekerjaan", "Ide", "To-Do", "Lainnya"]
        
        # Buat direktori jika belum ada
        os.makedirs(self.notes_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

    def generate_note_id(self):
        """Generate ID unik untuk catatan baru"""
        timestamp = datetime.now().strftime("%Y%m%d")
        existing_notes = len(os.listdir(self.notes_dir))
        return f"note_{timestamp}_{existing_notes+1:03d}"

    def create_note(self, title, category, content):
        """Membuat catatan baru"""
        if category not in self.categories:
            raise ValueError("Kategori tidak valid!")

        note = {
            "id": self.generate_note_id(),
            "title": title,
            "category": category,
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        filename = os.path.join(self.notes_dir, f"{note['id']}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(note, f, indent=4, ensure_ascii=False)
        
        return note

    def get_all_notes(self):
        """Mengambil semua catatan"""
        notes = []
        for filename in os.listdir(self.notes_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.notes_dir, filename), 'r', encoding='utf-8') as f:
                    notes.append(json.load(f))
        return sorted(notes, key=lambda x: x['created_at'], reverse=True)

    def get_note_by_id(self, note_id):
        """Mengambil catatan berdasarkan ID"""
        filename = os.path.join(self.notes_dir, f"{note_id}.json")
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def search_notes(self, keyword):
        """Mencari catatan berdasarkan kata kunci"""
        notes = self.get_all_notes()
        keyword = keyword.lower()
        return [
            note for note in notes
            if keyword in note['title'].lower() or
               keyword in note['content'].lower()
        ]

    def get_notes_by_date(self, date_str):
        """Mengambil catatan berdasarkan tanggal"""
        notes = self.get_all_notes()
        return [
            note for note in notes
            if note['created_at'].startswith(date_str)
        ]

    def get_notes_by_category(self, category):
        """Mengambil catatan berdasarkan kategori"""
        if category not in self.categories:
            raise ValueError("Kategori tidak valid!")
        
        notes = self.get_all_notes()
        return [
            note for note in notes
            if note['category'] == category
        ]

    def update_note(self, note_id, title=None, category=None, content=None):
        """Mengupdate catatan yang ada"""
        note = self.get_note_by_id(note_id)
        if not note:
            raise ValueError("Catatan tidak ditemukan!")

        if category and category not in self.categories:
            raise ValueError("Kategori tidak valid!")

        if title:
            note['title'] = title
        if category:
            note['category'] = category
        if content:
            note['content'] = content

        note['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        filename = os.path.join(self.notes_dir, f"{note_id}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(note, f, indent=4, ensure_ascii=False)
        
        return note

    def delete_note(self, note_id):
        """Menghapus catatan"""
        filename = os.path.join(self.notes_dir, f"{note_id}.json")
        if os.path.exists(filename):
            os.remove(filename)
            return True
        return False

    def create_backup(self):
        """Membuat backup dari semua catatan"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = os.path.join(self.backup_dir, f"backup_{timestamp}.zip")
        
        if os.listdir(self.notes_dir):
            shutil.make_archive(backup_filename[:-4], 'zip', self.notes_dir)
            return backup_filename
        return None

    def restore_backup(self, backup_file):
        """Memulihkan catatan dari file backup"""
        if not os.path.exists(backup_file):
            raise ValueError("File backup tidak ditemukan!")

        # Buat direktori temporary untuk ekstraksi
        temp_dir = os.path.join(self.backup_dir, "temp")
        os.makedirs(temp_dir, exist_ok=True)

        try:
            # Ekstrak backup
            shutil.unpack_archive(backup_file, temp_dir)
            
            # Hapus catatan yang ada
            for file in os.listdir(self.notes_dir):
                os.remove(os.path.join(self.notes_dir, file))
            
            # Pindahkan file dari backup
            for file in os.listdir(temp_dir):
                shutil.move(
                    os.path.join(temp_dir, file),
                    os.path.join(self.notes_dir, file)
                )
            
            return True
            
        except Exception as e:
            raise Exception(f"Gagal memulihkan backup: {str(e)}")
        
        finally:
            # Bersihkan direktori temporary
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)