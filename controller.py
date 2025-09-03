
from model import HangmanModel, Verdict


class HangmanController:
    def __init__(self, answer: str, lives: int) -> None:
        self._model = HangmanModel(answer, lives)

    def guess(self, char: str) -> Verdict:
        return self._model.make_guess(char)

    def progress(self) -> str:
        return self._model.get_current_progress()

    def guesses(self) -> list[str]:
        return self._model.get_all_guesses()

    def lives(self) -> int:
        return self._model.lives_left

    def is_done(self) -> bool:
        return self._model.is_game_done

    def did_win(self) -> bool:
        return self._model.did_player_win

    def did_lose(self) -> bool:
        return self._model.did_player_lose

    def final_answer(self) -> str | None:
        return self._model.answer
