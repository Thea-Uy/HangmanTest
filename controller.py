from model import HangmanModel


class HangmanController:
    def __init__(self, word: str, lives: int) -> None:
        self.model = HangmanModel(word, lives)

    def get_current_progress(self) -> str:
        return self.model.get_current_progress()

    def get_all_guesses(self) -> list[str]:
        return self.model.get_all_guesses()

    def get_lives_left(self) -> int:
        return self.model.lives_left

    def get_answer(self) -> str | None:
        return self.model.answer

    def get_answer_for_display(self) -> str:
        return self.model.get_answer_for_display()

    def has_already_guessed(self, guess: str) -> bool:
        return self.model.has_already_guessed(guess)

    def is_valid_guess(self, guess: str) -> bool:
        return self.model.is_valid_guess(guess)

    def make_guess(self, guess: str) -> None:
        if self.model.did_player_win or self.model.did_player_lose:
            return  # Ignore guesses after game ends
        if not self.is_valid_guess(guess):
            return  # Ignore invalid guess
        if self.has_already_guessed(guess):
            return  # Ignore duplicate guess
        self.model.make_guess(guess)

    def player_won(self) -> bool:
        return self.model.did_player_win

    def player_lost(self) -> bool:
        return self.model.did_player_lose


