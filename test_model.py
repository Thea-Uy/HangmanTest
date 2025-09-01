from model import HangmanModel, Verdict


# Constructor tests
def test_init_empty_answer():
    """Test that empty answer raises ValueError."""
    try:
        HangmanModel("", 5)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_init_nonpositive_lives():
    """Test that zero or negative lives raises ValueError."""
    try:
        HangmanModel("aloha", 0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    try:
        HangmanModel("aloha", -1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_init_constraint_violations():
    """Test constraint violations for answer length, lives count, and non-alphanumeric."""
    try:
        HangmanModel("masyadongmahaba", 5)  # > 10 chars
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    try:
        HangmanModel("aloha", 11)  # > 10 lives
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    try:
        HangmanModel("aloha!", 5)  # Non-alphanumeric
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_init_valid():
    """Test valid initialization."""
    model = HangmanModel("aloha", 5)
    assert model.lives_left == 5
    assert not model.did_player_win
    assert not model.did_player_lose
    assert not model.is_game_done
    assert model.answer is None
    assert model.guesses == set()


# Invalid guess tests
def test_make_guess_invalid_empty():
    """Test invalid guess with empty string."""
    model = HangmanModel("aloha", 5)
    verdict = model.make_guess("")

    assert verdict == Verdict.INVALID
    assert model.lives_left == 5
    assert len(model.guesses) == 0


def test_make_guess_invalid_multiple_chars():
    """Test invalid guess with multiple characters."""
    model = HangmanModel("aloha", 5)
    verdict = model.make_guess("hello")

    assert verdict == Verdict.INVALID
    assert model.lives_left == 5
    assert len(model.guesses) == 0


def test_make_guess_invalid_non_alphanumeric():
    """Test invalid guess with non-alphanumeric character."""
    model = HangmanModel("aloha", 5)
    verdict = model.make_guess("!")

    assert verdict == Verdict.INVALID
    assert model.lives_left == 5
    assert len(model.guesses) == 0


# Already guessed tests
def test_make_guess_already_guessed():
    """Test making the same guess twice."""
    model = HangmanModel("aloha", 5)
    model.make_guess("a")
    verdict = model.make_guess("a")

    assert verdict == Verdict.ALREADY_GUESSED
    assert model.lives_left == 5
    assert len(model.guesses) == 1


def test_make_guess_already_guessed_case_insensitive():
    """Test that already guessed is case insensitive."""
    model = HangmanModel("Aloha", 5)
    model.make_guess("a")
    verdict = model.make_guess("A")

    assert verdict == Verdict.ALREADY_GUESSED
    assert model.lives_left == 5


# Correct guess tests
def test_make_guess_correct():
    """Test making a correct guess."""
    model = HangmanModel("aloha", 5)
    verdict = model.make_guess("a")

    assert verdict == Verdict.CORRECT
    assert model.lives_left == 5
    assert "a" in model.guesses
    assert not model.is_game_done


def test_make_guess_correct_with_digits():
    """Test correct guess with digits."""
    model = HangmanModel("wandat1", 5)
    verdict = model.make_guess("1")

    assert verdict == Verdict.CORRECT
    assert model.lives_left == 5
    assert "1" in model.guesses


def test_make_guess_correct_case_insensitive():
    """Test correct guess is case insensitive."""
    model = HangmanModel("Aloha", 5)
    verdict = model.make_guess("a")

    assert verdict == Verdict.CORRECT
    assert model.lives_left == 5


# Incorrect guess tests
def test_make_guess_incorrect():
    """Test making an incorrect guess."""
    model = HangmanModel("aloha", 5)
    verdict = model.make_guess("x")

    assert verdict == Verdict.INCORRECT
    assert model.lives_left == 4
    assert "x" in model.guesses
    assert not model.is_game_done


# Win condition tests
def test_make_guess_win_condition():
    """Test winning by guessing all letters."""
    model = HangmanModel("wow", 5)
    model.make_guess("w")
    verdict = model.make_guess("o")

    assert verdict == Verdict.CORRECT
    assert model.did_player_win
    assert model.is_game_done
    assert model.answer == "wow"


def test_make_guess_win_single_character():
    """Test winning with single character word."""
    model = HangmanModel("a", 5)
    verdict = model.make_guess("a")

    assert verdict == Verdict.CORRECT
    assert model.did_player_win
    assert model.is_game_done


# Loss condition tests
def test_make_guess_lose_condition():
    """Test losing by running out of lives."""
    model = HangmanModel("aloha", 1)
    verdict = model.make_guess("x")

    assert verdict == Verdict.INCORRECT
    assert model.did_player_lose
    assert model.is_game_done
    assert model.lives_left == 0
    assert model.answer == "aloha"


def test_make_guess_lose_multiple_incorrect():
    """Test losing with multiple incorrect guesses."""
    model = HangmanModel("wow", 3)
    model.make_guess("x")
    model.make_guess("y")
    verdict = model.make_guess("z")

    assert verdict == Verdict.INCORRECT
    assert model.did_player_lose
    assert model.is_game_done


# Game done tests
def test_make_guess_when_game_done_after_win():
    """Test that guesses are ignored after winning."""
    model = HangmanModel("wow", 5)
    model.make_guess("w")
    model.make_guess("o")  # Win
    verdict = model.make_guess("x")

    assert verdict == Verdict.GAME_DONE
    assert model.did_player_win
    assert model.lives_left == 5


def test_make_guess_when_game_done_after_loss():
    """Test that guesses are ignored after losing."""
    model = HangmanModel("aloha", 1)
    model.make_guess("x")  # Lose
    verdict = model.make_guess("a")

    assert verdict == Verdict.GAME_DONE
    assert model.did_player_lose
    assert model.lives_left == 0


# Answer property tests
def test_answer_hidden_during_game():
    """Test that answer is None during game."""
    model = HangmanModel("aloha", 5)
    model.make_guess("a")

    assert model.answer is None
    assert not model.is_game_done


def test_answer_revealed_after_win():
    """Test that answer is revealed after winning."""
    model = HangmanModel("wow", 5)
    model.make_guess("w")
    model.make_guess("o")

    assert model.answer == "wow"


def test_answer_revealed_after_loss():
    """Test that answer is revealed after losing."""
    model = HangmanModel("aloha", 1)
    model.make_guess("x")

    assert model.answer == "aloha"


# Answer state tests
def test_answer_state_partial_reveal():
    """Test answer_state shows correct progress with original casing."""
    model = HangmanModel("Aloha", 5)

    # Initially all hidden
    initial_state = list(model.answer_state)
    assert all(char is None for char in initial_state)
    assert len(initial_state) == 5

    # After guessing 'a'
    model.make_guess("a")
    state_after_a = list(model.answer_state)
    assert state_after_a[0] == "A"  # Original casing preserved
    assert state_after_a[1] is None
    assert state_after_a[2] is None
    assert state_after_a[3] is None
    assert state_after_a[4] == "a"  # Both 'a' characters revealed


def test_answer_state_complete_reveal():
    """Test answer_state when all letters are guessed."""
    model = HangmanModel("wow", 5)
    model.make_guess("w")
    model.make_guess("o")

    state = list(model.answer_state)
    assert state == ["w", "o", "w"]


# Guesses tracking tests
def test_guesses_tracking():
    """Test that guesses are tracked correctly."""
    model = HangmanModel("aloha", 5)
    model.make_guess("a")
    model.make_guess("x")
    model.make_guess("invalid_guess")  # Should not be added

    assert model.guesses == {"a", "x"}


def test_guesses_immutable_copy():
    """Test that guesses property returns a copy."""
    model = HangmanModel("aloha", 5)
    model.make_guess("a")

    guesses = model.guesses
    guesses.add("should_not_affect_model")

    assert "should_not_affect_model" not in model.guesses
