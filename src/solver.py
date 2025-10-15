from copy import deepcopy
from random import sample
from tqdm import tqdm

class Solver():
    def __init__(self, words: list[str]):
        self.words: list[str] = words
        self.greens: list[tuple[int, str]] = []
        self.yellows: list[tuple[int, str]] = []
        self.grays: list[str] = []

        self.starters = ["soare", "tales", "cones", "salet"]
        self.possible_words = words
        self.scores = {}

    def reset(self):
        self.possible_words = self.words

    def add_guess(self, results: str, word: str):
        """
        Add a guess, where each letter in the str corrosponds to Green (A), Yellow (B) or Gray (C)
        """
        results = results.lower()
        for i in range(5):
            score = results[i]
            if score == "2" or score == "g": self.greens.append((i, word[i]))
            elif score == "1" or score == "y": self.yellows.append((i, word[i]))
            elif word[i] not in [l for _, l in self.greens] and word[i] not in [l for _, l in self.yellows]:
                self.grays.append(word[i])
            
    def set_possible_words(self):
        possible_words = []
        for word in self.possible_words:
            ok = True
            for pos, letter in self.greens:
                if word[pos] != letter:
                    ok = False
                    break
            if not ok: continue
            for pos, letter in self.yellows:
                if letter not in word or word[pos] == letter:
                    ok = False
                    break
            if not ok: continue
            for letter in self.grays:
                if letter in word:
                    ok = False
                    break
            if not ok: continue

            possible_words.append(word)
        self.possible_words = possible_words

    def get_guess(self, guess_count: int = 1000, result_count: int = 1000, words_removed_count: int = 1000) -> tuple[str, str]:
        guess_count = min(len(self.possible_words), guess_count)
        best_guess = None
        best_score = 0
        for guess in tqdm(sample(self.possible_words, guess_count)):
            score = self.test_guess(guess, result_count, words_removed_count)
            if score > best_score:
                best_guess = guess
                best_score = score
        return best_guess, best_score
    
    def test_guess(self, guess: str, result_count: int = 1000, words_removed_count: int = 1000):
        result_count = min(len(self.possible_words), result_count)
        words_removed_count = min(len(self.possible_words), words_removed_count)
        words_removed = 0
        for result in sample(self.possible_words, result_count):
            greens = deepcopy(self.greens)
            yellows = deepcopy(self.yellows)
            grays = deepcopy(self.grays)
            for i in range(5):
                if guess[i] == result[i]: greens.append((i, guess[i]))
                elif guess[i] in result:
                    if guess[i] not in yellows: yellows.append((i, guess[i]))
                elif guess[i] not in [l for _, l in greens] and guess[i] not in [l for _, l in yellows]:
                    grays.append(guess[i])
            words_removed += self.get_words_removed(greens, yellows, grays, words_removed_count)
        return words_removed / result_count
            
    def get_words_removed(self, greens, yellows, grays, words_removed_count: int = 1000):
        words_removed = words_removed_count
        for word in sample(self.possible_words, words_removed_count):
            ok = True
            for pos, letter in greens:
                if word[pos] != letter:
                    ok = False
                    break
            if not ok: continue
            for pos, letter in yellows:
                if letter not in word or word[pos] == letter:
                    ok = False
                    break
            if not ok: continue
            for letter in grays:
                if letter in word:
                    ok = False
                    break
            if not ok: continue
            words_removed -= 1
        return words_removed