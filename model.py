from enum import StrEnum, auto


class Verdict(StrEnum):
    CORRECT = auto()
    INCORRECT = auto()
    INVALID = auto()
    ALREADY_GUESSED = auto()
    GAME_DONE = auto()


class HangmanModel:
    def __init__(self, answer: str, lives: int) -> None:
        if not answer:
            raise ValueError("your answer is empty")
        if lives <= 0:
            raise ValueError("lives must be at least 1")

        self._original_answer = answer
        self._answer = answer.lower()
        self._lives_left = lives
        self._starting_lives = lives

        self._correct_guesses: set[str] = set()
        self._incorrect_guesses: set[str] = set()
        self._game_over = False
        self._player_winner = False

    def make_guess(self, guess: str) -> Verdict:
        verdict = self._check_guess(guess)

        match verdict:
            case Verdict.GAME_DONE:
                return verdict
            case Verdict.CORRECT:
                g = guess.lower()
                self._correct_guesses.add(g)
                if all(ch in self._correct_guesses for ch in set(self._answer)):
                    self._game_over = True
                    self._player_winner = True
            case Verdict.INCORRECT:
                g = guess.lower()
                self._incorrect_guesses.add(g)
                self._lives_left -= 1
                if self._lives_left <= 0:
                    self._game_over = True
            case _:
                pass  
        return verdict

    def _check_guess(self, guess: str) -> Verdict:
        if self._game_over:
            return Verdict.GAME_DONE
        if not self.is_valid_guess(guess):
            return Verdict.INVALID

        g = guess.lower()
        if g in self._correct_guesses or g in self._incorrect_guesses:
            return Verdict.ALREADY_GUESSED
        if g in self._answer:
            return Verdict.CORRECT
        return Verdict.INCORRECT


    def get_all_guesses(self) -> list[str]:
        return sorted(self._correct_guesses | self._incorrect_guesses)

    def is_valid_guess(self, guess: str) -> bool:
        return len(guess) == 1 and guess.isalnum()

    def has_already_guessed(self, guess: str) -> bool:
        if not self.is_valid_guess(guess):
            return False
        g = guess.lower()
        return g in self._correct_guesses or g in self._incorrect_guesses

    def get_current_progress(self) -> str:
        return " ".join(
            ch if ch in self._correct_guesses else "_"
            for ch in self._answer
        )

    def get_answer_for_display(self) -> str:
        return self._answer

    @property
    def answer(self) -> str | None:
        return self._original_answer if self._game_over else None

    @property
    def lives_left(self) -> int:
        return self._lives_left

    @property
    def did_player_win(self) -> bool:
        return self._game_over and self._player_winner

    @property
    def did_player_lose(self) -> bool:
        return self._game_over and not self._player_winner

    @property
    def is_game_done(self) -> bool:
        return self._game_over



