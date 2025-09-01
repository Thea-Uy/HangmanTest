from enum import StrEnum, auto


class Verdict(StrEnum):
    """Possible outcomes when making a guess."""
    CORRECT = auto()
    INCORRECT = auto()
    INVALID = auto()
    ALREADY_GUESSED = auto()
    GAME_DONE = auto()


class HangmanModel:
    """Model for Hangman game implementing all game logic."""

    def __init__(self, answer: str, lives: int) -> None:
        """Initialize a new Hangman game."""
        if not answer:
            raise ValueError("Answer cannot be empty")
        if lives <= 0:
            raise ValueError("Lives must be positive")

        # Enforce lab constraints
        if len(answer) > 10:
            raise ValueError("Answer too long (max 10 characters)")
        if lives > 10:
            raise ValueError("Too many lives (max 10)")
        if not answer.isalnum():
            raise ValueError("Answer must be alphanumeric")

        # Store both original and normalized answers
        self._original_answer: str = answer
        self._norm_answer: str = answer.lower()
        self._lives_left: int = lives
        self._guesses: set[str] = set()
        self._correct_guesses: set[str] = set()
        self._is_game_over: bool = False
        self._did_player_win: bool = False

    def make_guess(self, guess: str) -> Verdict:
        """Process a player's guess and update game state."""
        verdict = self._check_guess(guess)

        if verdict == Verdict.GAME_DONE:
            return verdict

        match verdict:
            case Verdict.CORRECT:
                normalized_guess = guess.lower()
                self._guesses.add(normalized_guess)
                self._correct_guesses.add(normalized_guess)
                # Check if player won
                if all(char in self._correct_guesses for char in self._norm_answer):
                    self._is_game_over = True
                    self._did_player_win = True
            case Verdict.INCORRECT:
                self._guesses.add(guess.lower())
                self._lives_left -= 1
                # Check if player lost
                if self._lives_left == 0:
                    self._is_game_over = True
            case _:
                pass  # Invalid and already guessed don't change state

        return verdict

    def _check_guess(self, guess: str) -> Verdict:
        """Validate a guess and determine its verdict without changing state."""
        # Check if game is already over
        if self._is_game_over:
            return Verdict.GAME_DONE

        # Validate input format first (before normalization)
        if len(guess) != 1 or not guess.isalnum():
            return Verdict.INVALID

        # Normalize guess for comparison after validation
        normalized_guess = guess.lower()

        match True:
            case _ if normalized_guess in self._guesses:
                return Verdict.ALREADY_GUESSED
            case _ if normalized_guess in self._norm_answer:
                return Verdict.CORRECT
            case _:
                return Verdict.INCORRECT

    @property
    def answer(self) -> str | None:
        """Return the original answer if game is over, None otherwise."""
        return self._original_answer if self._is_game_over else None

    @property
    def lives_left(self) -> int:
        """Return the current number of lives remaining."""
        return self._lives_left

    @property
    def did_player_win(self) -> bool:
        """Return True if game is over and player won."""
        return self._is_game_over and self._did_player_win

    @property
    def did_player_lose(self) -> bool:
        """Return True if game is over and player lost."""
        return self._is_game_over and not self._did_player_win

    @property
    def guesses(self) -> set[str]:
        """Return a copy of all guesses made so far."""
        return self._guesses.copy()

    @property
    def answer_state(self) -> list[str | None]:
        """Return current state showing revealed characters in original casing."""
        return [
            self._original_answer[i] if self._norm_answer[i] in self._correct_guesses else None
            for i in range(len(self._original_answer))
        ]

    @property
    def is_game_done(self) -> bool:
        """Return True if the game has ended (win or loss)."""
        return self._is_game_over
