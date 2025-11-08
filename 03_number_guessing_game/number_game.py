import random
import json
import os
from datetime import datetime

class NumberGame:
    def __init__(self):
        self.highscores_file = "highscores.json"
        self.difficulties = {
            'mudah': {'range': (1, 50), 'max_guesses': 10, 'penalty': 10},
            'sedang': {'range': (1, 100), 'max_guesses': 7, 'penalty': 14},
            'sulit': {'range': (1, 200), 'max_guesses': 5, 'penalty': 20}
        }
        self.load_highscores()

    def load_highscores(self):
        """Memuat data high score dari file"""
        try:
            if os.path.exists(self.highscores_file):
                with open(self.highscores_file, 'r') as file:
                    self.highscores = json.load(file)
            else:
                self.highscores = {'mudah': [], 'sedang': [], 'sulit': []}
        except Exception:
            self.highscores = {'mudah': [], 'sedang': [], 'sulit': []}

    def save_highscores(self):
        """Menyimpan data high score ke file"""
        try:
            with open(self.highscores_file, 'w') as file:
                json.dump(self.highscores, file)
        except Exception as e:
            print(f"Error menyimpan high score: {str(e)}")

    def add_score(self, difficulty, score, guesses):
        """Menambahkan skor baru ke daftar high score"""
        date = datetime.now().strftime("%Y-%m-%d")
        self.highscores[difficulty].append({
            'score': score,
            'guesses': guesses,
            'date': date
        })
        # Urutkan dan ambil 5 skor tertinggi
        self.highscores[difficulty] = sorted(
            self.highscores[difficulty],
            key=lambda x: (-x['score'], x['guesses'])
        )[:5]
        self.save_highscores()

    def show_highscores(self, difficulty):
        """Menampilkan daftar high score"""
        print(f"\n=== High Scores ({difficulty.upper()}) ===")
        scores = self.highscores[difficulty]
        if not scores:
            print("Belum ada skor yang tercatat.")
            return
        
        for i, score in enumerate(scores, 1):
            print(f"{i}. Skor: {score['score']} (Tebakan: {score['guesses']}) - {score['date']}")

    def get_hint(self, guess, target, difficulty):
        """Memberikan petunjuk untuk tebakan"""
        if difficulty == 'sulit':
            diff = abs(target - guess)
            if diff <= 10:
                return "Sangat Panas! 🔥"
            elif diff <= 20:
                return "Panas! 🌡️"
            elif diff <= 40:
                return "Hangat 😊"
            elif diff <= 80:
                return "Dingin ❄️"
            else:
                return "Sangat Dingin! 🧊"
        else:
            if guess < target:
                return "Terlalu kecil! ⬆️"
            else:
                return "Terlalu besar! ⬇️"

    def play_game(self):
        """Fungsi utama permainan"""
        print("\n=== Selamat Datang di Game Tebak Angka ===")
        print("\nPilih tingkat kesulitan:")
        print("1. Mudah (1-50, 10 tebakan)")
        print("2. Sedang (1-100, 7 tebakan)")
        print("3. Sulit (1-200, 5 tebakan)")

        # Pilih tingkat kesulitan
        while True:
            choice = input("\nPilihan Anda (1/2/3): ")
            if choice in ['1', '2', '3']:
                difficulty = ['mudah', 'sedang', 'sulit'][int(choice)-1]
                break
            print("Pilihan tidak valid!")

        # Set up permainan berdasarkan tingkat kesulitan
        diff_settings = self.difficulties[difficulty]
        number_range = diff_settings['range']
        max_guesses = diff_settings['max_guesses']
        penalty = diff_settings['penalty']
        target_number = random.randint(*number_range)
        
        print(f"\nSaya telah memilih angka antara {number_range[0]} dan {number_range[1]}")
        print(f"Anda punya {max_guesses} kesempatan untuk menebak!")
        print("Skor awal: 100\n")

        guesses = 0
        score = 100
        
        # Main game loop
        while guesses < max_guesses:
            try:
                guess = int(input(f"Tebakan #{guesses + 1}: "))
                
                if guess < number_range[0] or guess > number_range[1]:
                    print(f"Angka harus antara {number_range[0]} dan {number_range[1]}!")
                    continue

                guesses += 1

                if guess == target_number:
                    print(f"\n🎉 Selamat! Anda berhasil menebak angka {target_number}!")
                    print(f"Jumlah tebakan: {guesses}")
                    print(f"Skor akhir: {score}")
                    
                    self.add_score(difficulty, score, guesses)
                    self.show_highscores(difficulty)
                    return True

                hint = self.get_hint(guess, target_number, difficulty)
                score = max(0, score - penalty)
                print(f"{hint} (Skor: {score})")

            except ValueError:
                print("Masukkan angka yang valid!")
                continue

        print(f"\n😢 Maaf, Anda kehabisan kesempatan. Angka yang benar adalah {target_number}")
        print(f"Skor akhir: 0")
        self.show_highscores(difficulty)
        return False

def main():
    game = NumberGame()
    
    while True:
        game.play_game()
        play_again = input("\nMain lagi? (y/n): ").lower()
        if play_again != 'y':
            print("\nTerima kasih telah bermain! 👋")
            break

if __name__ == "__main__":
    main()