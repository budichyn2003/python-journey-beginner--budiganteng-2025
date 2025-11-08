from todo_manager import TodoManager
from datetime import datetime, date
import calendar
import os

# ANSI Color codes untuk tampilan berwarna
COLORS = {
    'HEADER': '\033[95m',
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m'
}

def clear_screen():
    """Membersihkan layar terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color):
    """Mencetak teks dengan warna"""
    print(f"{COLORS[color]}{text}{COLORS['ENDC']}")

def get_priority_color(priority):
    """Mendapatkan warna berdasarkan prioritas"""
    return {
        'Tinggi': 'RED',
        'Sedang': 'YELLOW',
        'Rendah': 'GREEN'
    }.get(priority, 'BLUE')

def print_task(task):
    """Menampilkan detail tugas dengan format yang bagus"""
    print("\n" + "="*50)
    print_colored(f"ID        : {task['id']}", 'HEADER')
    print_colored(f"Judul     : {task['title']}", 'BOLD')
    print(f"Deskripsi : {task['description']}")
    print_colored(f"Prioritas : {task['priority']}", get_priority_color(task['priority']))
    print(f"Kategori  : {task['category']}")
    print(f"Status    : {task['status']}")
    print(f"Progress  : {task['progress']}%")
    print(f"Due Date  : {task['due_date']}")
    print(f"Dibuat    : {task['created_at']}")
    if task['completed_at']:
        print(f"Selesai   : {task['completed_at']}")
    print("="*50)

def get_valid_date():
    """Mendapatkan input tanggal yang valid dari pengguna"""
    while True:
        date_str = input("Masukkan tanggal (YYYY-MM-DD): ")
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("Format tanggal tidak valid! Gunakan YYYY-MM-DD")

def add_task(manager):
    """Menu menambah tugas baru"""
    print_colored("\n=== Tambah Tugas Baru ===", 'HEADER')
    
    title = input("Judul tugas: ").strip()
    while not title:
        print("Judul tidak boleh kosong!")
        title = input("Judul tugas: ").strip()

    description = input("Deskripsi tugas: ").strip()
    
    print("\nKategori yang tersedia:")
    for i, category in enumerate(manager.categories, 1):
        print(f"{i}. {category}")
    while True:
        try:
            choice = int(input("Pilih kategori (1-5): "))
            if 1 <= choice <= len(manager.categories):
                category = manager.categories[choice-1]
                break
        except ValueError:
            pass
        print("Pilihan tidak valid!")

    print("\nPrioritas:")
    for i, priority in enumerate(manager.priorities, 1):
        print_colored(f"{i}. {priority}", get_priority_color(priority))
    while True:
        try:
            choice = int(input("Pilih prioritas (1-3): "))
            if 1 <= choice <= len(manager.priorities):
                priority = manager.priorities[choice-1]
                break
        except ValueError:
            pass
        print("Pilihan tidak valid!")

    due_date = get_valid_date()

    try:
        task = manager.add_task(title, description, category, priority, due_date)
        print_colored("\nTugas berhasil ditambahkan!", 'GREEN')
        print_task(task)
    except Exception as e:
        print_colored(f"\nError: {str(e)}", 'RED')

def view_tasks(manager):
    """Menu melihat tugas"""
    while True:
        print_colored("\n=== Lihat Tugas ===", 'HEADER')
        print("1. Semua tugas")
        print("2. Filter berdasarkan status")
        print("3. Filter berdasarkan prioritas")
        print("4. Filter berdasarkan kategori")
        print("5. Tampilan kalender")
        print("6. Tugas yang lewat deadline")
        print("7. Kembali ke menu utama")

        choice = input("\nPilihan Anda (1-7): ")

        if choice == '1':
            tasks = manager.get_all_tasks()
            if not tasks:
                print_colored("\nBelum ada tugas!", 'YELLOW')
                continue
            for task in tasks:
                print_task(task)

        elif choice == '2':
            print("\nStatus yang tersedia:")
            for i, status in enumerate(manager.statuses, 1):
                print(f"{i}. {status}")
            try:
                choice = int(input("Pilih status (1-4): "))
                if 1 <= choice <= len(manager.statuses):
                    status = manager.statuses[choice-1]
                    tasks = manager.get_tasks_by_status(status)
                    if not tasks:
                        print_colored(f"\nTidak ada tugas dengan status {status}!", 'YELLOW')
                        continue
                    for task in tasks:
                        print_task(task)
            except ValueError:
                print_colored("Pilihan tidak valid!", 'RED')

        elif choice == '3':
            print("\nPrioritas:")
            for i, priority in enumerate(manager.priorities, 1):
                print_colored(f"{i}. {priority}", get_priority_color(priority))
            try:
                choice = int(input("Pilih prioritas (1-3): "))
                if 1 <= choice <= len(manager.priorities):
                    priority = manager.priorities[choice-1]
                    tasks = manager.get_tasks_by_priority(priority)
                    if not tasks:
                        print_colored(f"\nTidak ada tugas dengan prioritas {priority}!", 'YELLOW')
                        continue
                    for task in tasks:
                        print_task(task)
            except ValueError:
                print_colored("Pilihan tidak valid!", 'RED')

        elif choice == '4':
            print("\nKategori yang tersedia:")
            for i, category in enumerate(manager.categories, 1):
                print(f"{i}. {category}")
            try:
                choice = int(input("Pilih kategori (1-5): "))
                if 1 <= choice <= len(manager.categories):
                    category = manager.categories[choice-1]
                    tasks = manager.get_tasks_by_category(category)
                    if not tasks:
                        print_colored(f"\nTidak ada tugas dalam kategori {category}!", 'YELLOW')
                        continue
                    for task in tasks:
                        print_task(task)
            except ValueError:
                print_colored("Pilihan tidak valid!", 'RED')

        elif choice == '5':
            today = date.today()
            cal = calendar.monthcalendar(today.year, today.month)
            
            print_colored(f"\n{calendar.month_name[today.month]} {today.year}", 'HEADER')
            print("Mo Tu We Th Fr Sa Su")
            
            for week in cal:
                for day in week:
                    if day == 0:
                        print("  ", end=" ")
                    else:
                        date_str = f"{today.year}-{today.month:02d}-{day:02d}"
                        tasks_today = [t for t in manager.tasks if t['due_date'] == date_str]
                        if tasks_today:
                            print_colored(f"{day:2d}", 'RED', end=" ")
                        else:
                            print(f"{day:2d}", end=" ")
                print()

            input("\nTekan Enter untuk melanjutkan...")

        elif choice == '6':
            tasks = manager.get_overdue_tasks()
            if not tasks:
                print_colored("\nTidak ada tugas yang melewati deadline!", 'GREEN')
                continue
            print_colored("\nTugas yang melewati deadline:", 'RED')
            for task in tasks:
                print_task(task)

        elif choice == '7':
            break

def update_task(manager):
    """Menu mengupdate tugas"""
    print_colored("\n=== Update Tugas ===", 'HEADER')
    tasks = manager.get_all_tasks()
    if not tasks:
        print_colored("Belum ada tugas!", 'YELLOW')
        return

    print("\nDaftar Tugas:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. [{task['status']}] {task['title']} (Due: {task['due_date']})")

    try:
        choice = int(input("\nPilih nomor tugas (0 untuk batal): "))
        if choice == 0:
            return
        if 1 <= choice <= len(tasks):
            task = tasks[choice-1]
            print_task(task)

            print("\nBagian yang akan diupdate:")
            print("1. Status")
            print("2. Progress")
            print("3. Detail tugas")
            print("4. Batal")

            update_choice = input("\nPilihan Anda (1-4): ")

            if update_choice == '1':
                print("\nStatus yang tersedia:")
                for i, status in enumerate(manager.statuses, 1):
                    print(f"{i}. {status}")
                try:
                    status_choice = int(input("Pilih status (1-4): "))
                    if 1 <= status_choice <= len(manager.statuses):
                        new_status = manager.statuses[status_choice-1]
                        updated_task = manager.update_task_status(task['id'], new_status)
                        print_colored("Status berhasil diupdate!", 'GREEN')
                        print_task(updated_task)
                except ValueError:
                    print_colored("Pilihan tidak valid!", 'RED')

            elif update_choice == '2':
                try:
                    progress = int(input("Masukkan progress (0-100): "))
                    updated_task = manager.update_task_progress(task['id'], progress)
                    print_colored("Progress berhasil diupdate!", 'GREEN')
                    print_task(updated_task)
                except ValueError as e:
                    print_colored(f"Error: {str(e)}", 'RED')

            elif update_choice == '3':
                print("\nKosongkan input jika tidak ingin mengubah")
                title = input("Judul baru: ").strip()
                description = input("Deskripsi baru: ").strip()
                
                category = None
                print("\nKategori yang tersedia:")
                for i, cat in enumerate(manager.categories, 1):
                    print(f"{i}. {cat}")
                try:
                    cat_choice = int(input("Pilih kategori (0 untuk skip): "))
                    if 1 <= cat_choice <= len(manager.categories):
                        category = manager.categories[cat_choice-1]
                except ValueError:
                    pass

                priority = None
                print("\nPrioritas:")
                for i, prio in enumerate(manager.priorities, 1):
                    print_colored(f"{i}. {prio}", get_priority_color(prio))
                try:
                    prio_choice = int(input("Pilih prioritas (0 untuk skip): "))
                    if 1 <= prio_choice <= len(manager.priorities):
                        priority = manager.priorities[prio_choice-1]
                except ValueError:
                    pass

                due_date = None
                if input("Update due date? (y/n): ").lower() == 'y':
                    due_date = get_valid_date()

                try:
                    updated_task = manager.update_task_details(
                        task['id'],
                        title=title if title else None,
                        description=description if description else None,
                        category=category,
                        priority=priority,
                        due_date=due_date
                    )
                    print_colored("Tugas berhasil diupdate!", 'GREEN')
                    print_task(updated_task)
                except Exception as e:
                    print_colored(f"Error: {str(e)}", 'RED')

        else:
            print_colored("Pilihan tidak valid!", 'RED')
    except ValueError:
        print_colored("Input tidak valid!", 'RED')

def delete_task(manager):
    """Menu menghapus tugas"""
    print_colored("\n=== Hapus Tugas ===", 'HEADER')
    print("1. Hapus satu tugas")
    print("2. Hapus semua tugas selesai")
    print("3. Kembali ke menu utama")

    choice = input("\nPilihan Anda (1-3): ")

    if choice == '1':
        tasks = manager.get_all_tasks()
        if not tasks:
            print_colored("Belum ada tugas!", 'YELLOW')
            return

        print("\nDaftar Tugas:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. [{task['status']}] {task['title']} (Due: {task['due_date']})")

        try:
            task_num = int(input("\nPilih nomor tugas (0 untuk batal): "))
            if task_num == 0:
                return
            if 1 <= task_num <= len(tasks):
                task = tasks[task_num-1]
                print_task(task)
                
                confirm = input("\nAnda yakin ingin menghapus tugas ini? (y/n): ")
                if confirm.lower() == 'y':
                    if manager.delete_task(task['id']):
                        print_colored("Tugas berhasil dihapus!", 'GREEN')
            else:
                print_colored("Pilihan tidak valid!", 'RED')
        except ValueError:
            print_colored("Input tidak valid!", 'RED')

    elif choice == '2':
        confirm = input("Anda yakin ingin menghapus semua tugas yang sudah selesai? (y/n): ")
        if confirm.lower() == 'y':
            count = manager.delete_completed_tasks()
            if count > 0:
                print_colored(f"{count} tugas selesai berhasil dihapus!", 'GREEN')
            else:
                print_colored("Tidak ada tugas selesai untuk dihapus!", 'YELLOW')

def main():
    """Fungsi utama program"""
    manager = TodoManager()
    
    while True:
        clear_screen()
        print_colored("=== Todo List CLI ===", 'HEADER')
        print("1. Tambah Tugas")
        print("2. Lihat Tugas")
        print("3. Update Tugas")
        print("4. Hapus Tugas")
        print("5. Keluar")

        choice = input("\nPilihan Anda (1-5): ")

        if choice == '1':
            add_task(manager)
        elif choice == '2':
            view_tasks(manager)
        elif choice == '3':
            update_task(manager)
        elif choice == '4':
            delete_task(manager)
        elif choice == '5':
            print_colored("\nTerima kasih telah menggunakan Todo List CLI!", 'BLUE')
            break
        else:
            print_colored("Pilihan tidak valid!", 'RED')
        
        input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    main()