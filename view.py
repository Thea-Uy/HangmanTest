from collections.abc import Sequence


class HangmanView:
    def prompt_guess(self) -> str:
        return input("Enter a letter: ")

    def show_correct_guess(self, guess: str):
        print(f"{guess} is correct")

    def show_incorrect_guess(self, guess: str):
        print(f"{guess} is incorrect")

    def show_invalid_guess(self, guess: str):
        print(f"{guess} is not a valid guess")

    def show_already_guessed(self, guess: str):
        print(f"You have already tried {guess}")

    def show_win(self, answer: str):
        print(f"You win! The answer is {answer}")

    def show_lose(self, answer: str):
        print(f"You lose! The answer is {answer}")

    def show_game_done(self):
        print("Game is done; no more guesses allowed")

    def show_lives_left(self, lives: int):
        print(f"Lives left: {lives}")

    def show_guesses(self, guesses: set[str]):
        print(f"Guesses: {', '.join(sorted(guesses))}")

    def show_answer_state(self, answer_state: Sequence[str | None]):
        display: list[str] = [
            "_" if ch is None else ch
            for ch in answer_state
        ]

        print(" ".join(display))