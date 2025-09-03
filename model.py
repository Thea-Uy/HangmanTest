
from enum import StrEnum, auto


class Verdict(StrEnum):
    CORRECT = auto()
    INCORRECT = auto()
    INVALID = auto()
    ALREADY_GUESSED = auto()
    GAME_DONE = auto()


class HangmanModel:
    """Model for Hangman game implementing all game logic."""

    def __init__(self, answer: str, lives: int) -> None:
        if not answer:
            raise ValueError("your answer is empty")
        if lives <= 0:
            raise ValueError("lives must be at least 1")

        self._answer: str = answer  # keep original casing
        self._lives_left: int = lives
        self._guesses: set[str] = set()
        self._correct_guesses: set[str] = set()
        self._is_game_over: bool = False
        self._did_player_win: bool = False

    def make_guess(self, guess: str) -> Verdict:
        verdict = self._check_guess(guess)

        if verdict == Verdict.GAME_DONE:
            return verdict

        g = guess.lower()
        if verdict == Verdict.CORRECT:
            self._guesses.add(g)
            self._correct_guesses.add(g)
            if all(ch.lower() in self._correct_guesses for ch in self._answer):
                self._is_game_over = True
                self._did_player_win = True
        elif verdict == Verdict.INCORRECT:
            self._guesses.add(g)
            self._lives_left -= 1
            if self._lives_left <= 0:
                self._is_game_over = True

        return verdict

    def _check_guess(self, guess: str) -> Verdict:
        if self._is_game_over:
            return Verdict.GAME_DONE
        if len(guess) != 1 or not guess.isalnum():
            return Verdict.INVALID

        g = guess.lower()
        if g in self._guesses:
            return Verdict.ALREADY_GUESSED
        if g in (ch.lower() for ch in self._answer):
            return Verdict.CORRECT
        return Verdict.INCORRECT

    # Properties
    @property
    def answer(self) -> str | None:
        return self._answer if self._is_game_over else None

    @property
    def lives_left(self) -> int:
        return self._lives_left

    @property
    def did_player_win(self) -> bool:
        return self._is_game_over and self._did_player_win

    @property
    def did_player_lose(self) -> bool:
        return self._is_game_over and not self._did_player_win

    # Helpers for controller/tests
    def get_all_guesses(self) -> list[str]:
        return sorted(self._guesses)

    def is_valid_guess(self, guess: str) -> bool:
        return len(guess) == 1 and guess.isalnum()

    def has_already_guessed(self, guess: str) -> bool:
        return len(guess) == 1 and guess.lower() in self._guesses

    def get_answer_for_display(self) -> str:
        """Reveal the answer fully (used at game end)."""
        return self._answer

    def get_current_progress(self) -> str:
        """Reveal guessed letters, hide others with underscores."""
        return " ".join(
            ch if ch.lower() in self._correct_guesses else "_"
            for ch in self._answer
        )
