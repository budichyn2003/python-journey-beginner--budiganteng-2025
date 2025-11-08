import json
import random
from datetime import datetime

class Quiz:
    def __init__(self, quiz_file="quiz_data.json"):
        """
        Inisialisasi Quiz
        Args:
            quiz_file (str): Path ke file JSON yang berisi data quiz
        """
        self.quiz_file = quiz_file
        self.quizzes = self.load_quizzes()
        self.current_quiz = None
        self.score = 0
        self.total_questions = 0
        self.current_question = 0
        self.answers = []

    def load_quizzes(self):
        """Load data quiz dari file JSON"""
        try:
            with open(self.quiz_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "categories": [],
                "quizzes": {}
            }

    def save_quizzes(self):
        """Simpan data quiz ke file JSON"""
        with open(self.quiz_file, 'w', encoding='utf-8') as f:
            json.dump(self.quizzes, f, indent=4, ensure_ascii=False)

    def get_categories(self):
        """Mendapatkan daftar kategori quiz yang tersedia"""
        return self.quizzes.get("categories", [])

    def add_category(self, category):
        """
        Menambahkan kategori baru
        Args:
            category (str): Nama kategori
        """
        if "categories" not in self.quizzes:
            self.quizzes["categories"] = []
        
        if category not in self.quizzes["categories"]:
            self.quizzes["categories"].append(category)
            if "quizzes" not in self.quizzes:
                self.quizzes["quizzes"] = {}
            self.quizzes["quizzes"][category] = []
            self.save_quizzes()

    def add_question(self, category, question, answers, correct_answer, explanation=""):
        """
        Menambahkan pertanyaan baru ke kategori tertentu
        
        Args:
            category (str): Kategori quiz
            question (str): Pertanyaan
            answers (list): Daftar pilihan jawaban
            correct_answer (int): Index jawaban yang benar (0-based)
            explanation (str): Penjelasan jawaban (optional)
        """
        if category not in self.get_categories():
            raise ValueError(f"Kategori {category} tidak ditemukan!")

        question_data = {
            "question": question,
            "answers": answers,
            "correct_answer": correct_answer,
            "explanation": explanation
        }

        self.quizzes["quizzes"][category].append(question_data)
        self.save_quizzes()

    def start_quiz(self, category, num_questions=None):
        """
        Memulai quiz baru
        
        Args:
            category (str): Kategori quiz
            num_questions (int): Jumlah pertanyaan yang diinginkan (optional)
        """
        if category not in self.get_categories():
            raise ValueError(f"Kategori {category} tidak ditemukan!")

        available_questions = self.quizzes["quizzes"][category]
        if not available_questions:
            raise ValueError(f"Tidak ada pertanyaan dalam kategori {category}!")

        if num_questions is None or num_questions > len(available_questions):
            num_questions = len(available_questions)

        self.current_quiz = {
            "category": category,
            "questions": random.sample(available_questions, num_questions),
            "start_time": datetime.now()
        }
        
        self.score = 0
        self.total_questions = num_questions
        self.current_question = 0
        self.answers = []

    def get_current_question(self):
        """Mendapatkan pertanyaan saat ini"""
        if not self.current_quiz or self.current_question >= len(self.current_quiz["questions"]):
            return None

        question_data = self.current_quiz["questions"][self.current_question]
        return {
            "question": question_data["question"],
            "answers": question_data["answers"],
            "number": self.current_question + 1,
            "total": self.total_questions
        }

    def submit_answer(self, answer_index):
        """
        Submit jawaban untuk pertanyaan saat ini
        
        Args:
            answer_index (int): Index jawaban yang dipilih
            
        Returns:
            dict: Hasil validasi jawaban
        """
        if not self.current_quiz or self.current_question >= len(self.current_quiz["questions"]):
            return None

        current_q = self.current_quiz["questions"][self.current_question]
        is_correct = answer_index == current_q["correct_answer"]
        
        if is_correct:
            self.score += 1

        result = {
            "is_correct": is_correct,
            "correct_answer": current_q["answers"][current_q["correct_answer"]],
            "explanation": current_q.get("explanation", ""),
            "score": self.score,
            "total": self.total_questions
        }

        self.answers.append({
            "question": current_q["question"],
            "user_answer": current_q["answers"][answer_index],
            "correct_answer": current_q["answers"][current_q["correct_answer"]],
            "is_correct": is_correct
        })

        self.current_question += 1
        return result

    def get_final_results(self):
        """Mendapatkan hasil akhir quiz"""
        if not self.current_quiz or self.current_question < self.total_questions:
            return None

        end_time = datetime.now()
        duration = end_time - self.current_quiz["start_time"]
        
        return {
            "category": self.current_quiz["category"],
            "score": self.score,
            "total_questions": self.total_questions,
            "percentage": (self.score / self.total_questions) * 100,
            "duration": str(duration).split('.')[0],  # Format: HH:MM:SS
            "answers": self.answers,
            "start_time": self.current_quiz["start_time"].strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def save_results(self, results, filename="quiz_results.json"):
        """
        Menyimpan hasil quiz ke file
        
        Args:
            results (dict): Hasil quiz
            filename (str): Nama file untuk menyimpan hasil
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except FileNotFoundError:
            history = []

        history.append(results)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)

    def get_results_history(self, filename="quiz_results.json"):
        """
        Mendapatkan history hasil quiz
        
        Args:
            filename (str): Nama file yang berisi history
            
        Returns:
            list: Daftar hasil quiz sebelumnya
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []