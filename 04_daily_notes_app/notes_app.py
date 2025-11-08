from notes_manager import NotesManager
import os
from datetime import datetime

def print_note(note):
    """Menampilkan detail catatan"""
    print("\n" + "="*50)
    print(f"ID        : {note['id']}")
    print(f"Judul     : {note['title']}")
    print(f"Kategori  : {note['category']}")
    print(f"Dibuat    : {note['created_at']}")
    print(f"Diupdate  : {note['updated_at']}")
    print("-"*50)
    print("Isi:")
    print(note['content'])
    print("="*50)

def get_valid_category(manager):
    """Mendapatkan kategori yang valid dari input pengguna"""
    while True:
        print("\nKategori yang tersedia:")
        for i, category in enumerate(manager.categories, 1):
            print(f"{i}. {category}")
        
        try:
            choice = int(input("\nPilih kategori (1-5): "))
            if 1 <= choice <= len(manager.categories):
                return manager.categories[choice-1]
        except ValueError:
            pass
        print("Pilihan tidak valid!")

def create_note(manager):
    """Menu membuat catatan baru"""
    print("\n=== Buat Catatan Baru ===")
    
    title = input("Judul catatan: ").strip()
    while not title:
        print("Judul tidak boleh kosong!")
        title = input("Judul catatan: ").strip()

    category = get_valid_category(manager)
    
    print("\nIsi catatan (ketik 'SELESAI' di baris baru untuk mengakhiri):")
    content_lines = []
    while True:
        line = input()
        if line == 'SELESAI':
            break
        content_lines.append(line)
    content = '\n'.join(content_lines)

    try:
        note = manager.create_note(title, category, content)
        print("\nCatatan berhasil dibuat!")
        print_note(note)
    except Exception as e:
        print(f"\nError: {str(e)}")

def view_notes(manager):
    """Menu melihat catatan"""
    while True:
        print("\n=== Lihat Catatan ===")
        print("1. Lihat semua catatan")
        print("2. Cari berdasarkan tanggal")
        print("3. Cari berdasarkan kategori")
        print("4. Cari berdasarkan kata kunci")
        print("5. Kembali ke menu utama")

        choice = input("\nPilihan Anda (1-5): ")

        if choice == '1':
            notes = manager.get_all_notes()
            if not notes:
                print("\nBelum ada catatan!")
                continue
            for note in notes:
                print_note(note)

        elif choice == '2':
            date = input("\nMasukkan tanggal (YYYY-MM-DD): ")
            try:
                datetime.strptime(date, '%Y-%m-%d')
                notes = manager.get_notes_by_date(date)
                if not notes:
                    print("\nTidak ada catatan pada tanggal tersebut!")
                    continue
                for note in notes:
                    print_note(note)
            except ValueError:
                print("Format tanggal tidak valid!")

        elif choice == '3':
            category = get_valid_category(manager)
            notes = manager.get_notes_by_category(category)
            if not notes:
                print(f"\nTidak ada catatan dalam kategori {category}!")
                continue
            for note in notes:
                print_note(note)

        elif choice == '4':
            keyword = input("\nMasukkan kata kunci: ")
            notes = manager.search_notes(keyword)
            if not notes:
                print("\nTidak ada catatan yang cocok!")
                continue
            for note in notes:
                print_note(note)

        elif choice == '5':
            break

def edit_note(manager):
    """Menu mengedit catatan"""
    print("\n=== Edit Catatan ===")
    notes = manager.get_all_notes()
    if not notes:
        print("Belum ada catatan!")
        return

    print("\nDaftar Catatan:")
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note['title']} ({note['created_at']})")

    try:
        choice = int(input("\nPilih nomor catatan yang akan diedit (0 untuk batal): "))
        if choice == 0:
            return
        if 1 <= choice <= len(notes):
            note = notes[choice-1]
            print_note(note)

            print("\nBagian yang akan diedit:")
            print("1. Judul")
            print("2. Kategori")
            print("3. Isi")
            print("4. Batal")

            edit_choice = input("\nPilihan Anda (1-4): ")
            
            if edit_choice == '1':
                new_title = input("Judul baru: ").strip()
                if new_title:
                    manager.update_note(note['id'], title=new_title)
                    print("Judul berhasil diupdate!")
            
            elif edit_choice == '2':
                new_category = get_valid_category(manager)
                manager.update_note(note['id'], category=new_category)
                print("Kategori berhasil diupdate!")
            
            elif edit_choice == '3':
                print("\nIsi baru (ketik 'SELESAI' di baris baru untuk mengakhiri):")
                content_lines = []
                while True:
                    line = input()
                    if line == 'SELESAI':
                        break
                    content_lines.append(line)
                new_content = '\n'.join(content_lines)
                manager.update_note(note['id'], content=new_content)
                print("Isi berhasil diupdate!")

        else:
            print("Pilihan tidak valid!")
    except ValueError:
        print("Input tidak valid!")
    except Exception as e:
        print(f"Error: {str(e)}")

def delete_note(manager):
    """Menu menghapus catatan"""
    print("\n=== Hapus Catatan ===")
    notes = manager.get_all_notes()
    if not notes:
        print("Belum ada catatan!")
        return

    print("\nDaftar Catatan:")
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note['title']} ({note['created_at']})")

    try:
        choice = int(input("\nPilih nomor catatan yang akan dihapus (0 untuk batal): "))
        if choice == 0:
            return
        if 1 <= choice <= len(notes):
            note = notes[choice-1]
            print_note(note)
            
            confirm = input("\nAnda yakin ingin menghapus catatan ini? (y/n): ")
            if confirm.lower() == 'y':
                if manager.delete_note(note['id']):
                    print("Catatan berhasil dihapus!")
                else:
                    print("Gagal menghapus catatan!")
        else:
            print("Pilihan tidak valid!")
    except ValueError:
        print("Input tidak valid!")

def backup_restore(manager):
    """Menu backup dan restore"""
    while True:
        print("\n=== Backup & Restore ===")
        print("1. Buat backup")
        print("2. Pulihkan dari backup")
        print("3. Kembali ke menu utama")

        choice = input("\nPilihan Anda (1-3): ")

        if choice == '1':
            try:
                backup_file = manager.create_backup()
                if backup_file:
                    print(f"Backup berhasil dibuat: {backup_file}")
                else:
                    print("Tidak ada catatan untuk di-backup!")
            except Exception as e:
                print(f"Error: {str(e)}")

        elif choice == '2':
            backups = [f for f in os.listdir(manager.backup_dir) if f.endswith('.zip')]
            if not backups:
                print("Tidak ada file backup!")
                continue

            print("\nFile backup yang tersedia:")
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup}")

            try:
                choice = int(input("\nPilih nomor file backup (0 untuk batal): "))
                if choice == 0:
                    continue
                if 1 <= choice <= len(backups):
                    backup_file = os.path.join(manager.backup_dir, backups[choice-1])
                    confirm = input("Proses ini akan menimpa semua catatan yang ada. Lanjutkan? (y/n): ")
                    if confirm.lower() == 'y':
                        try:
                            manager.restore_backup(backup_file)
                            print("Restore berhasil!")
                        except Exception as e:
                            print(f"Error: {str(e)}")
                else:
                    print("Pilihan tidak valid!")
            except ValueError:
                print("Input tidak valid!")

        elif choice == '3':
            break

def main():
    """Fungsi utama program"""
    manager = NotesManager()
    
    while True:
        print("\n=== Daily Notes App ===")
        print("1. Buat Catatan Baru")
        print("2. Lihat Catatan")
        print("3. Edit Catatan")
        print("4. Hapus Catatan")
        print("5. Backup & Restore")
        print("6. Keluar")

        choice = input("\nPilihan Anda (1-6): ")

        if choice == '1':
            create_note(manager)
        elif choice == '2':
            view_notes(manager)
        elif choice == '3':
            edit_note(manager)
        elif choice == '4':
            delete_note(manager)
        elif choice == '5':
            backup_restore(manager)
        elif choice == '6':
            print("\nTerima kasih telah menggunakan Daily Notes App!")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()