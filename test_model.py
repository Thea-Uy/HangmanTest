import pytest
from model import HangmanModel


class TestInit:
    def test_init_valid(self) -> None:
        model = HangmanModel("hello", 5)
        assert model.lives_left == 5
        assert not model.did_player_win
        assert not model.did_player_lose
        assert model.answer is None

    def test_empty_raise_error(self) -> None:
        with pytest.raises(ValueError, match="your answer is empty"):
            HangmanModel("", 5)

    def test_zero_lives_raise_error(self) -> None:
        with pytest.raises(ValueError, match="lives must be at least 1"):
            HangmanModel("hello", 0)

    def test_negative_lives_raises_error(self) -> None:
        with pytest.raises(ValueError, match="lives must be at least 1"):
            HangmanModel("hello", -1)


class TestGuessing:
    def test_correct_guess_lowercase(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("h")
        assert model.lives_left == 3
        assert "h" in model.get_all_guesses()
        assert model.has_already_guessed("h")

    def test_correct_guess_uppercase(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("H")
        assert model.lives_left == 3
        assert "h" in model.get_all_guesses()

    def test_incorrect_guess(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("x")
        assert model.lives_left == 2
        assert "x" in model.get_all_guesses()

    def test_number_as_guess_correct(self) -> None:
        model = HangmanModel("test123", 3)
        model.make_guess("1")
        assert model.lives_left == 3
        assert "1" in model.get_all_guesses()

    def test_number_as_guess_incorrect(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("1")
        assert model.lives_left == 2
        assert "1" in model.get_all_guesses()

    def test_invalid_guess_empty(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("")
        assert model.lives_left == 3
        assert len(model.get_all_guesses()) == 0

    def test_invalid_guess_mult_char(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("hello")
        assert model.lives_left == 3
        assert len(model.get_all_guesses()) == 0

    def test_duplicate_correct_guess(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("h")
        model.make_guess("h")
        assert model.lives_left == 3
        assert model.get_all_guesses().count("h") == 1

    def test_duplicate_incorrect_guess(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("x")
        model.make_guess("x")
        assert model.lives_left == 2
        assert model.get_all_guesses().count("x") == 1


class TestGameEnd:
    def test_win(self) -> None:
        model = HangmanModel("hi", 3)
        model.make_guess("h")
        model.make_guess("i")
        assert model.did_player_win
        assert model.answer == "hi"

    def test_lose(self) -> None:
        model = HangmanModel("hi", 1)
        model.make_guess("x")
        assert model.did_player_lose
        assert model.answer == "hi"

    def test_win_with_incorrects(self) -> None:
        model = HangmanModel("hi", 3)
        model.make_guess("x")
        model.make_guess("h")
        model.make_guess("i")
        assert model.did_player_win
        assert model.lives_left == 2


class TestUtility:
    def test_get_all_guesses_sorted(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("z")
        mo

