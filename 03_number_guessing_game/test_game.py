import unittest
import os
from number_game import NumberGame

class TestNumberGame(unittest.TestCase):
    def setUp(self):
        self.game = NumberGame()
        # Gunakan file test terpisah untuk highscores
        self.game.highscores_file = "test_highscores.json"

    def tearDown(self):
        # Hapus file test setelah pengujian
        if os.path.exists(self.game.highscores_file):
            os.remove(self.game.highscores_file)

    def test_initial_highscores(self):
        """Test inisialisasi high scores"""
        self.assertEqual(len(self.game.highscores), 3)
        self.assertIn('mudah', self.game.highscores)
        self.assertIn('sedang', self.game.highscores)
        self.assertIn('sulit', self.game.highscores)

    def test_add_score(self):
        """Test penambahan skor"""
        self.game.add_score('mudah', 80, 5)
        self.assertEqual(len(self.game.highscores['mudah']), 1)
        self.assertEqual(self.game.highscores['mudah'][0]['score'], 80)
        self.assertEqual(self.game.highscores['mudah'][0]['guesses'], 5)

    def test_highscore_sorting(self):
        """Test pengurutan high scores"""
        scores = [(80, 5), (90, 4), (70, 6), (100, 3), (85, 5), (95, 4)]
        for score, guesses in scores:
            self.game.add_score('mudah', score, guesses)
        
        # Periksa apakah hanya 5 skor teratas yang disimpan
        self.assertEqual(len(self.game.highscores['mudah']), 5)
        
        # Periksa urutan skor (dari tinggi ke rendah)
        scores = [score['score'] for score in self.game.highscores['mudah']]
        self.assertEqual(scores, [100, 95, 90, 85, 80])

    def test_get_hint_easy_medium(self):
        """Test hint untuk level mudah dan sedang"""
        # Test untuk tebakan yang terlalu kecil
        hint = self.game.get_hint(5, 10, 'mudah')
        self.assertEqual(hint, "Terlalu kecil! ⬆️")
        
        # Test untuk tebakan yang terlalu besar
        hint = self.game.get_hint(15, 10, 'sedang')
        self.assertEqual(hint, "Terlalu besar! ⬇️")

    def test_get_hint_hard(self):
        """Test hint untuk level sulit"""
        # Test berbagai jarak tebakan
        hints = [
            (95, 100, "Sangat Panas! 🔥"),    # diff = 5
            (85, 100, "Panas! 🌡️"),           # diff = 15
            (70, 100, "Hangat 😊"),           # diff = 30
            (150, 100, "Dingin ❄️"),          # diff = 50
            (10, 100, "Sangat Dingin! 🧊")    # diff = 90
        ]
        
        for guess, target, expected in hints:
            hint = self.game.get_hint(guess, target, 'sulit')
            self.assertEqual(hint, expected)

    def test_difficulty_settings(self):
        """Test pengaturan tingkat kesulitan"""
        # Test range angka
        self.assertEqual(self.game.difficulties['mudah']['range'], (1, 50))
        self.assertEqual(self.game.difficulties['sedang']['range'], (1, 100))
        self.assertEqual(self.game.difficulties['sulit']['range'], (1, 200))
        
        # Test maksimum tebakan
        self.assertEqual(self.game.difficulties['mudah']['max_guesses'], 10)
        self.assertEqual(self.game.difficulties['sedang']['max_guesses'], 7)
        self.assertEqual(self.game.difficulties['sulit']['max_guesses'], 5)
        
        # Test pengurangan skor
        self.assertEqual(self.game.difficulties['mudah']['penalty'], 10)
        self.assertEqual(self.game.difficulties['sedang']['penalty'], 14)
        self.assertEqual(self.game.difficulties['sulit']['penalty'], 20)

if __name__ == '__main__':
    unittest.main()