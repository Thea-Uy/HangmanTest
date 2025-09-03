from collections.abc import Sequence
from model import HangmanModel
from view import HangmanView

class HangmanController:
	def __init__(self, model: HangmanModel, view: HangmanView) -> None:
		self.model = model
		self.view = view

	def start(self) -> None:
		while not (self.model.did_player_win or self.model.did_player_lose):
			self.display_game_state()

			guess = self.view.prompt_guess()

			self.check_guess(guess)


		self.display_game_end()

	def display_game_state(self) -> None:
		answer_state = self.answer_state()
		self.view.show_answer_state(answer_state)

		guesses = set(self.model.get_all_guesses())
		self.view.show_guesses(guesses)

		self.view.show_lives_left(self.model.lives_left)

	def answer_state(self) -> Sequence[str | None]:
		answer = self.model.display_answer()
		guessed = set(self.model.get_all_guesses())

		return [character if character in guessed else None for character in answer]

	def check_guess(self, guess: str) -> None:
		if not self.model.guess_is_valid(guess):
			self.view.show_invalid_guess(guess)
			return
		if self.model.guess_is_already_guessed(guess):
			self.view.show_already_guessed(guess)
			return

		self.model.make_guess(guess)
		guess_lower = guess.lower()
		guess_is_correct = guess_lower in self.model._correct_guesses

		if guess_is_correct:
			self.view.show_correct_guess(guess)
		else:
			self.view.show_incorrect_guess(guess)

	def display_game_end(self) -> None:
		answer = self.model.answer or self.model.display_answer()

		if self.model.did_player_win:
			self.view.show_win(answer or "")
		else:
			self.view.show_lose(answer or "")
