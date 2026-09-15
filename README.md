# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
- Run `pytest` in your terminal.
- Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.** This is a number-guessing game built with Streamlit where the player picks a difficulty level, then tries to guess a randomly generated secret number within a limited number of attempts, using "higher/lower" hints along the way.
- [x] **Detail which bugs you found.** I found three bugs: the hint messages were swapped (telling the player to guess higher when they actually needed to go lower, and vice versa), clicking "New Game" reset the attempts counter but never reset the game's status, leaving it permanently stuck on "Game over" until the page was refreshed, and the scoring logic randomly added points for a wrong "Too High" guess instead of always deducting them.
- [x] **Explain what fixes you applied.** I fixed the swapped hint messages and the inconsistent scoring inside `check_guess()` and `update_score()`, and moved both functions out of `app.py` into `logic_utils.py` as part of the refactor. I documented the "New Game" soft-lock bug in `reflection.md` but intentionally left it unfixed, focusing my two required fixes on the hint and scoring bugs instead.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. The user opens the app and selects a difficulty (Easy, Normal, or Hard) from the sidebar, which sets the guessing range and number of allowed attempts.
2. The user opens "Developer Debug Info" to see the secret number for testing purposes — for example, the secret is 42.
3. The user enters a guess of 20 and clicks "Submit Guess." Since 20 is below 42, the game correctly responds "📈 Go HIGHER!" and the score decreases by 5 points.
4. The user enters a guess of 60. Since 60 is above 42, the game correctly responds "📉 Go LOWER!" and the score decreases by another 5 points.
5. The user enters a guess of 42 exactly. The game displays "🎉 Correct!", shows a balloon animation, and reports the final score based on how many attempts were used.
6. If the user instead runs out of attempts without guessing correctly, the game displays "Out of attempts! The secret was [number]." along with the final score.

## 🧪 Test Results

```
=================================== test session starts ===================================
platform darwin -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0 -- /Library/Frameworks/Python.framework/Versions/3.14/bin/python3
cachedir: .pytest_cache
rootdir: /Users/shaniahsmith/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.15.1
collected 9 items

tests/test_game_logic.py::test_winning_guess PASSED                                 [ 11%]
tests/test_game_logic.py::test_guess_too_high PASSED                                [ 22%]
tests/test_game_logic.py::test_guess_too_low PASSED                                 [ 33%]
tests/test_game_logic.py::test_hint_message_when_guess_too_high PASSED              [ 44%]
tests/test_game_logic.py::test_hint_message_when_guess_too_low PASSED               [ 55%]
tests/test_game_logic.py::test_score_deducts_on_too_high_regardless_of_attempt_parity PASSED [ 66%]
tests/test_game_logic.py::test_score_deducts_on_too_low PASSED                      [ 77%]
tests/test_game_logic.py::test_score_awards_points_on_win PASSED                    [ 88%]
tests/test_game_logic.py::test_multiple_wrong_guesses_keep_lowering_score PASSED    [100%]

==================================== 9 passed in 0.02s ====================================
```
