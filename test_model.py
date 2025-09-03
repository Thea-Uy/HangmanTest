import pytest
from model import HangmanModel


class Init:
    def init(self) -> None:
        model = HangmanModel("hello", 5)
        assert model.lives_left == 5
        assert not model.did_player_win
        assert not model.did_player_lose
        assert model.answer is None
    
    def empty_raise_error(self) -> None:
        with pytest.raises(ValueError, match="your answer is empty"):
            HangmanModel("", 5)
    
    def zero_lives_raise_error(self) -> None:
        with pytest.raises(ValueError, match="lives must be at least 1"):
            HangmanModel("hello", 0)
    
    def negative_lives_raises_error(self) -> None:
        with pytest.raises(ValueError, match="lives must be at least 1"):
            HangmanModel("hello", -1)


class Guessing:
    def correct_guess_lowercase(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("h")
        
        assert model.lives_left == 3
        assert "h" in model.get_all_guesses()
        assert model.has_already_guessed("h")
    
    def correct_guess_uppercase(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("H")
        
        assert model.lives_left == 3
        assert "h" in model.get_all_guesses()
        assert model.has_already_guessed("h")
    
    def incorrect_guess(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("x")
        
        assert model.lives_left == 2
        assert "x" in model.get_all_guesses()
        assert not model.did_player_win
    
    def number_as_guess_correct(self) -> None:
        model = HangmanModel("test123", 3)
        model.make_guess("1")
        
        assert model.lives_left == 3  # No life lost
        assert "1" in model.get_all_guesses()
    
    def number_as_guess_incorrect(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("1")
        
        assert model.lives_left == 2
        assert "1" in model.get_all_guesses()
    
    def invalid_guess_empty(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("")
        
        assert model.lives_left == 3
        assert len(model.get_all_guesses()) == 0
    
    def invalid_guess_mult_char(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("hello")
        
        assert model.lives_left == 3 
        assert len(model.get_all_guesses()) == 0
    
    def duplicate_correct_guess(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("h")
        model.make_guess("h") 
        
        assert model.lives_left == 3 
        assert model.get_all_guesses().count("h") == 1 
    
    def duplicate_incorrect_guess(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("x")
        model.make_guess("x")
        
        assert model.lives_left == 2  
        assert model.get_all_guesses().count("x") == 1 
    
    def case_insensitive_duplicate(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("h")
        model.make_guess("H") 

        assert model.lives_left == 3
        assert len(model.get_all_guesses()) == 1
        assert "h" in model.get_all_guesses()


class GameEnd:
    def win(self) -> None:
        model = HangmanModel("hi", 3)
        model.make_guess("h")
        model.make_guess("i")
        
        assert model.did_player_win
        assert not model.did_player_lose
        assert model.answer == "hi"

    def lose(self) -> None:
        model = HangmanModel("hello", 2)
        model.make_guess("x")  
        model.make_guess("y")  
        
        assert model.lives_left == 0
        assert model.did_player_lose
        assert not model.did_player_win
        assert model.answer == "hello" 

    def win_with_incorrect_guesses(self) -> None:
        model = HangmanModel("hi", 3)
        model.make_guess("x") 
        model.make_guess("h")  
        model.make_guess("i")  
        
        assert model.lives_left == 2
        assert model.did_player_win
        assert not model.did_player_lose
    
    def guesses_ignored_after_win(self) -> None:
        model = HangmanModel("hi", 3)
        model.make_guess("h")
        model.make_guess("i")  
        
        lives_after_win = model.lives_left
        model.make_guess("x")  
        
        assert model.lives_left == lives_after_win  
        assert model.did_player_win 
    
    def guesses_ignored_after_lose(self) -> None:
        model = HangmanModel("hello", 1)
        model.make_guess("x")  
        
        assert model.did_player_lose
        
        model.make_guess("h")  
        assert model.did_player_lose 
        assert "h" not in model.get_all_guesses() 

class UsedByController:
    def test_get_all_guesses_sorted(self) -> None:
        model = HangmanModel("hello", 5)
        model.make_guess("z")
        model.make_guess("a")
        model.make_guess("m")
        
        guesses = model.get_all_guesses()
        assert guesses == ["a", "m", "z"]
    
    def get_all_guesses_empty(self) -> None:
        model = HangmanModel("hello", 3)
        guesses = model.get_all_guesses()
        assert guesses == []
    
    def is_valid_guess_one_char(self) -> None:
        model = HangmanModel("hello", 3)
        assert model.is_valid_guess("a")
        assert model.is_valid_guess("1")
        assert model.is_valid_guess("Z")
    
    def is_valid_guess_invalid(self) -> None:
        model = HangmanModel("hello", 3)
        assert not model.is_valid_guess("")
        assert not model.is_valid_guess("ab")
        assert not model.is_valid_guess("hello")
    
    def has_already_guessed_true(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("h")
        model.make_guess("x")
        
        assert model.has_already_guessed("h")
        assert model.has_already_guessed("H")
        assert model.has_already_guessed("x")
    
    def has_already_guessed_false(self) -> None:
        model = HangmanModel("hello", 3)
        model.make_guess("h")
        
        assert not model.has_already_guessed("e")
        assert not model.has_already_guessed("z")
    
    def has_already_guessed_invalid(self) -> None:
        model = HangmanModel("hello", 3)
        assert not model.has_already_guessed("")
        assert not model.has_already_guessed("ab")
    
    def get_answer_for_display(self) -> None:
        model = HangmanModel("HeLLo", 3)
        assert model.get_answer_for_display() == "hello"


class EdgeCases:
    def single_letter_word(self) -> None:
        model = HangmanModel("a", 2)
        model.make_guess("a")
        
        assert model.did_player_win
        assert model.get_current_progress() == "a"
    
    def repeated_letters_in_word(self) -> None:
        model = HangmanModel("aaa", 3)
        model.make_guess("a")
        
        assert model.did_player_win
        assert model.get_current_progress() == "a a a"
    
    def upper_and_lower_cases(self) -> None:
        model = HangmanModel("HeLLo", 3)
        model.make_guess("h")
        model.make_guess("E")
        
        assert "h" in model.get_all_guesses()
        assert "e" in model.get_all_guesses()
        assert model.has_already_guessed("h")
        assert model.has_already_guessed("e")
    
    def num_in_word(self) -> None:
        model = HangmanModel("test123", 5)
        
        for char in "test123":
            model.make_guess(char)
        
        assert model.did_player_win
        assert model.answer == "test123"
    
    def use_exactly_all_lives(self) -> None:
        model = HangmanModel("ab", 2)
        model.make_guess("x")
        model.make_guess("y") 
        
        assert model.did_player_lose
        assert model.lives_left == 0
    
    def test_win_on_last_life(self) -> None:

        model = HangmanModel("ab", 2)
        model.make_guess("x")  
        model.make_guess("a")  
        model.make_guess("b")  
        
        assert model.did_player_win
        assert model.lives_left == 1