from logic_utils import check_guess, update_score


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_hint_message_when_guess_too_high():
    # FIX: guessing too high should tell the player to go LOWER, not higher.
    # This targets the exact bug we found where the hint text was swapped.
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message.upper()


def test_hint_message_when_guess_too_low():
    # FIX: guessing too low should tell the player to go HIGHER, not lower.
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message.upper()


def test_score_deducts_on_too_high_regardless_of_attempt_parity():
    # FIX: a "Too High" wrong guess should always cost points, no matter
    # whether the attempt number is even or odd. This targets the scoring
    # bug where the old code randomly added +5 on even attempts instead.
    score_on_odd_attempt = update_score(current_score=0, outcome="Too High", attempt_number=3)
    score_on_even_attempt = update_score(current_score=0, outcome="Too High", attempt_number=4)
    assert score_on_odd_attempt == -5
    assert score_on_even_attempt == -5


def test_score_deducts_on_too_low():
    score = update_score(current_score=0, outcome="Too Low", attempt_number=1)
    assert score == -5


def test_score_awards_points_on_win():
    score = update_score(current_score=0, outcome="Win", attempt_number=1)
    assert score > 0


def test_multiple_wrong_guesses_keep_lowering_score():
    # FIX: reproduces the exact scenario we found manually — three wrong
    # guesses in a row used to bounce the score back up partway through
    # instead of continuing to decrease every time.
    score = 0
    score = update_score(current_score=score, outcome="Too Low", attempt_number=2)
    score = update_score(current_score=score, outcome="Too High", attempt_number=3)
    score = update_score(current_score=score, outcome="Too High", attempt_number=4)
    assert score == -15