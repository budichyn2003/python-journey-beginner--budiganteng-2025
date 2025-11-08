import click
from quiz import Quiz
from rich.console import Console
from rich.table import Table
from rich import box
import json
import os

console = Console()

def validate_quiz_file(quiz_file):
    """Memvalidasi dan membuat file quiz jika belum ada"""
    if not os.path.exists(quiz_file):
        initial_data = {
            "categories": ["Python", "JavaScript", "General Knowledge"],
            "quizzes": {
                "Python": [
                    {
                        "question": "Apa ekstensi file Python?",
                        "answers": [".py", ".pyth", ".pt", ".python"],
                        "correct_answer": 0,
                        "explanation": "File Python menggunakan ekstensi .py"
                    }
                ],
                "JavaScript": [
                    {
                        "question": "Apa keyword untuk mendefinisikan variabel di JavaScript?",
                        "answers": ["var", "let", "const", "Semua benar"],
                        "correct_answer": 3,
                        "explanation": "JavaScript mendukung var, let, dan const untuk deklarasi variabel"
                    }
                ],
                "General Knowledge": [
                    {
                        "question": "Apa ibukota Indonesia?",
                        "answers": ["Jakarta", "Bandung", "Surabaya", "Medan"],
                        "correct_answer": 0,
                        "explanation": "Jakarta adalah ibukota Indonesia"
                    }
                ]
            }
        }
        with open(quiz_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, indent=4, ensure_ascii=False)

def display_categories(categories):
    """Menampilkan daftar kategori yang tersedia"""
    table = Table(title="Kategori Quiz yang Tersedia", box=box.ROUNDED)
    table.add_column("No", justify="right", style="cyan")
    table.add_column("Kategori", style="green")
    
    for idx, category in enumerate(categories, 1):
        table.add_row(str(idx), category)
        
    console.print(table)

def display_question(question_data):
    """Menampilkan pertanyaan dengan format yang bagus"""
    console.print(f"\n[cyan]Pertanyaan {question_data['number']} dari {question_data['total']}[/cyan]")
    console.print(f"\n[yellow]{question_data['question']}[/yellow]\n")
    
    for idx, answer in enumerate(question_data['answers'], 1):
        console.print(f"{idx}. {answer}")

def display_result(result):
    """Menampilkan hasil jawaban"""
    if result['is_correct']:
        console.print("\n[green]✓ Benar![/green]")
    else:
        console.print(f"\n[red]✗ Salah![/red]")
        console.print(f"Jawaban yang benar: [green]{result['correct_answer']}[/green]")
    
    if result['explanation']:
        console.print(f"\n[blue]Penjelasan:[/blue] {result['explanation']}")
    
    console.print(f"\nSkor: [cyan]{result['score']}/{result['total']}[/cyan]")

def display_final_results(results):
    """Menampilkan hasil akhir quiz"""
    console.print("\n[bold cyan]═══ Hasil Quiz ═══[/bold cyan]")
    console.print(f"\nKategori: [yellow]{results['category']}[/yellow]")
    console.print(f"Waktu Mulai: {results['start_time']}")
    console.print(f"Waktu Selesai: {results['end_time']}")
    console.print(f"Durasi: {results['duration']}")
    console.print(f"\nSkor Akhir: [green]{results['score']}/{results['total_questions']}[/green]")
    console.print(f"Persentase: [green]{results['percentage']:.1f}%[/green]\n")
    
    # Tampilkan detail jawaban
    table = Table(title="Detail Jawaban", box=box.ROUNDED)
    table.add_column("No", justify="right", style="cyan")
    table.add_column("Pertanyaan", style="yellow")
    table.add_column("Jawaban Anda", style="blue")
    table.add_column("Status", justify="center")
    
    for idx, answer in enumerate(results['answers'], 1):
        status = "[green]✓[/green]" if answer['is_correct'] else "[red]✗[/red]"
        table.add_row(
            str(idx),
            answer['question'],
            answer['user_answer'],
            status
        )
        
    console.print(table)

@click.group()
def cli():
    """Aplikasi Quiz Interaktif"""
    pass

@cli.command()
@click.option('--quiz-file', default='quiz_data.json', help='File JSON untuk data quiz')
def start(quiz_file):
    """Mulai quiz baru"""
    try:
        # Validasi dan inisialisasi file quiz
        validate_quiz_file(quiz_file)
        
        # Inisialisasi quiz
        quiz = Quiz(quiz_file)
        categories = quiz.get_categories()
        
        if not categories:
            console.print("[red]Tidak ada kategori quiz yang tersedia![/red]")
            return
            
        # Tampilkan kategori
        display_categories(categories)
        
        # Pilih kategori
        while True:
            try:
                choice = int(console.input("\nPilih kategori (nomor): ")) - 1
                if 0 <= choice < len(categories):
                    category = categories[choice]
                    break
                console.print("[red]Pilihan tidak valid![/red]")
            except ValueError:
                console.print("[red]Mohon masukkan nomor yang valid![/red]")
        
        # Mulai quiz
        quiz.start_quiz(category)
        
        # Loop pertanyaan
        while True:
            question = quiz.get_current_question()
            if not question:
                break
                
            display_question(question)
            
            # Dapatkan jawaban
            while True:
                try:
                    answer = int(console.input("\nMasukkan jawaban (1-4): ")) - 1
                    if 0 <= answer < len(question['answers']):
                        break
                    console.print("[red]Pilihan tidak valid![/red]")
                except ValueError:
                    console.print("[red]Mohon masukkan nomor yang valid![/red]")
            
            # Submit dan tampilkan hasil
            result = quiz.submit_answer(answer)
            display_result(result)
            console.input("\nTekan Enter untuk melanjutkan...")
            console.clear()
        
        # Tampilkan hasil akhir
        results = quiz.get_final_results()
        display_final_results(results)
        
        # Simpan hasil
        quiz.save_results(results)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@cli.command()
@click.option('--results-file', default='quiz_results.json', help='File JSON untuk history hasil')
def history(results_file):
    """Tampilkan history hasil quiz"""
    try:
        quiz = Quiz()
        results = quiz.get_results_history(results_file)
        
        if not results:
            console.print("[yellow]Belum ada history quiz![/yellow]")
            return
            
        table = Table(title="History Quiz", box=box.ROUNDED)
        table.add_column("No", justify="right", style="cyan")
        table.add_column("Tanggal", style="blue")
        table.add_column("Kategori", style="yellow")
        table.add_column("Skor", justify="right", style="green")
        table.add_column("Durasi", style="magenta")
        
        for idx, result in enumerate(results, 1):
            table.add_row(
                str(idx),
                result['start_time'],
                result['category'],
                f"{result['score']}/{result['total_questions']} ({result['percentage']:.1f}%)",
                result['duration']
            )
            
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@cli.command()
@click.option('--quiz-file', default='quiz_data.json', help='File JSON untuk data quiz')
def add(quiz_file):
    """Tambah pertanyaan baru"""
    try:
        # Inisialisasi quiz
        quiz = Quiz(quiz_file)
        
        # Tampilkan kategori yang ada
        categories = quiz.get_categories()
        if categories:
            console.print("\n[cyan]Kategori yang tersedia:[/cyan]")
            for cat in categories:
                console.print(f"- {cat}")
        
        # Input kategori
        category = console.input("\nMasukkan kategori (baru/existing): ").strip()
        if category not in categories:
            if click.confirm(f"Kategori '{category}' belum ada. Buat kategori baru?"):
                quiz.add_category(category)
            else:
                return
        
        # Input pertanyaan
        question = console.input("\nMasukkan pertanyaan: ").strip()
        
        # Input pilihan jawaban
        console.print("\nMasukkan 4 pilihan jawaban:")
        answers = []
        for i in range(4):
            answer = console.input(f"{i+1}. ").strip()
            answers.append(answer)
        
        # Input jawaban yang benar
        while True:
            try:
                correct = int(console.input("\nNomor jawaban yang benar (1-4): ")) - 1
                if 0 <= correct < 4:
                    break
                console.print("[red]Pilihan tidak valid![/red]")
            except ValueError:
                console.print("[red]Mohon masukkan nomor yang valid![/red]")
        
        # Input penjelasan (optional)
        explanation = console.input("\nPenjelasan (optional): ").strip()
        
        # Tambahkan pertanyaan
        quiz.add_question(category, question, answers, correct, explanation)
        console.print("[green]Pertanyaan berhasil ditambahkan![/green]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == '__main__':
    cli()