from src.solver import Solver

def main():
    # Load words from file
    with open("words.txt", "r") as file:
        words = [line.strip() for line in file.readlines()]

    solver = Solver(words)

    print("Welcome to the Wordle helper!")
    print("Here are some good words to start with:", solver.starters)
    print("For entering results, use the format where 0 = grey, 1 = yellow, 2 = green")

    while True:
        word = input("Enter your guessed word: ").strip().lower()
        results = input("Enter the result of your guess: ").strip()
        solver.add_guess(results, word)
        solver.set_possible_words()
        print("Some possible words:", solver.possible_words[0:min(len(solver.possible_words), 5)])
        print("Best next guess:", solver.get_guess(guess_count=1000, result_count=400, words_removed_count=100))

if __name__ == "__main__":
    main()