from model import HangmanModel, Verdict
from view import HangmanView


class HangmanController:
    """Controller that coordinates between HangmanModel and HangmanView."""

    def __init__(self, model: HangmanModel, view: HangmanView) -> None:
        """Initialize controller with model and view components."""
        self._model: HangmanModel = model
        self._view: HangmanView = view

    def start(self) -> None:
        """Start the game and handle the main game loop."""
        model = self._model
        view = self._view

        # Show initial state before first prompt
        view.show_answer_state(model.answer_state)
        view.show_guesses(model.guesses)
        view.show_lives_left(model.lives_left)

        while not model.is_game_done:
            # Get guess and process it
            guess: str = view.prompt_guess()
            verdict: Verdict = model.make_guess(guess)

            # Show verdict result immediately, but if this guess finishes the game,
            # show the final win/lose message instead of the regular verdict.
            match verdict:
                case Verdict.INVALID:
                    view.show_invalid_guess(guess)
                case Verdict.ALREADY_GUESSED:
                    view.show_already_guessed(guess)
                case Verdict.CORRECT:
                    # If this correct guess made the player win, show win immediately
                    if model.did_player_win:
                        answer = model.answer
                        assert answer is not None
                        view.show_win(answer)
                        break
                    view.show_correct_guess(guess)
                case Verdict.INCORRECT:
                    # If this incorrect guess made the player lose, show lose immediately
                    if model.did_player_lose:
                        answer = model.answer
                        assert answer is not None
                        view.show_lose(answer)
                        break
                    view.show_incorrect_guess(guess)
                case Verdict.GAME_DONE:
                    view.show_game_done()
                    break  # Don't show state again

            # Show updated state only if game continues
            view.show_answer_state(model.answer_state)
            view.show_guesses(model.guesses)
            view.show_lives_left(model.lives_left)
