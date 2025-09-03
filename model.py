class HangmanModel:

    def __init__(self, answer: str, lives: int) -> None:
        if not answer:
            raise ValueError("your answer is empty")
        if lives <= 0:
            raise ValueError("lives must be at least 1")

        self._answer = answer.lower()
        
        self._starting_lives = lives
        self._lives_left = lives

        self._correct_guesses: set[str] = set()
        self._incorrect_guesses: set[str] = set()

        self._game_over = False
        self._player_winner = False



    def make_guess(self, guess: str):
        if len(guess) != 1:
            return 
        if self._game_over == True:
            return

        guess_lower = guess.lower()

        if guess_lower in self._correct_guesses or guess_lower in self._incorrect_guesses:
            return

        if guess_lower in self._answer:
            self._correct_guesses.add(guess_lower)
        else:
            self._incorrect_guesses.add(guess_lower)
            self._lives_left -= 1

        self.check_game_state()

    def check_game_state(self) -> None:
        guessed_the_answer = set(self._answer)
        if guessed_the_answer <= self._correct_guesses and self._lives_left > 0:
            self._game_over = True
            self._player_winner = True
        elif self._lives_left <= 0:
            self._game_over = True
            self._player_winner = False

    @property
    def answer(self) -> str | None:
        return self._answer if self._game_over == True else None

    @property
    def lives_left(self) -> int:
        return self._lives_left

    @property
    def did_player_win(self) -> bool:
        return True if self._game_over and self._player_winner else False

    @property
    def did_player_lose(self) -> bool:
        return True if self._game_over and not self._player_winner else False

    def get_all_guesses(self) -> list[str]:
        all_guesses = self._correct_guesses | self._incorrect_guesses
        return sorted(all_guesses)

    def guess_is_valid(self, guess: str) -> bool:
        return True if len(guess) == 1 else False

    def guess_is_already_guessed(self, guess: str) -> bool:
        if len(guess) != 1:
            return False
        return guess.lower() in self._incorrect_guesses or guess in self._correct_guesses

    def display_answer(self) -> str:
        return self._answer