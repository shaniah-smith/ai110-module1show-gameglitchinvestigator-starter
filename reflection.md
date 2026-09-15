# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The first time I ran the game, it looked like a normal number-guessing game
built in Streamlit, with a sidebar for difficulty, a guess input, and a
Developer Debug Info panel showing the secret number, attempts, and score.
It looked fully functional at a glance, but playing through it revealed
three real bugs: the hint messages pointed the wrong direction (telling me
to go higher when I needed to go lower, and vice versa), clicking "New
Game" after finishing a round left the game permanently stuck on "Game
over" instead of actually starting a new round, and the score changed
inconsistently on wrong guesses, sometimes going up instead of down.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guessed 2 when the secret was 84 | Hint should say "Go HIGHER!" | Hint said "Go LOWER!" | No crash — silent wrong hint |
| Guessed 81 when the secret was 80 | Hint should say "Go LOWER!" | Hint said "Go HIGHER!" | No crash — silent wrong hint |
| Completed a game (won or lost), then clicked "New Game" | Game should fully reset and accept new guesses | Attempts counter reset, but the game stayed stuck on "Game over" and Submit Guess did nothing | No crash — app permanently stuck until the page was refreshed |
| Guessed 79 (Too Low), then 81 twice (Too High) against a secret of 80 | Score should change consistently on every wrong guess | Score went 0 → -5 → -10 → -5, increasing back up on the third wrong guess | No crash — silent inconsistent scoring |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used Claude (in a chat conversation) as my AI coding assistant for this
entire project. One example of a correct suggestion: after I described the
hint bug, the AI read the actual check_guess() code and identified that the
hint messages were swapped between the "Too High" and "Too Low" branches. I
verified this myself by running "python3 -c" directly against logic_utils.py
to call check_guess(60, 50) and check_guess(40, 50), confirming the fixed
messages were correct independent of the Streamlit app or the browser.

One suggestion I didn't just accept blindly: before actually reading my real
app.py code, the AI's first theory about the hint bug involved a type-mismatch
issue where the secret number was being turned into a string every other
guess. Once I pasted the actual code, the AI corrected itself and found the
real, simpler cause (the hint text was just swapped). I made sure to have it
re-check against my actual file rather than trust the first explanation,
since it turned out to be based on guessing rather than the real source.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was really fixed by testing it multiple ways: first
manually in the running Streamlit app (submitting guesses above and below
the secret and checking the hint direction), and then more rigorously by
running "python3 -c" to call check_guess() and update_score() directly,
bypassing the browser entirely. This was important because I ran into a
confusing situation where an old, stale Streamlit process was still running
on port 8501 and showing the old buggy behavior even after my code was
fixed — testing the functions directly in Python proved the code itself was
correct, and restarting Streamlit on a fresh port fixed the display issue.
For automated testing, I ran "python3 -m pytest tests/test_game_logic.py -v"
and confirmed all tests passed, including new tests I added specifically
for the hint-direction and scoring bugs. The AI helped me design those
tests by pointing out that the starter tests were comparing the wrong thing
(check_guess returns a tuple, not a plain string) and by suggesting specific
test cases that would fail under the old buggy code but pass under the fix,
like checking that a "Too High" outcome always deducts points regardless of
whether the attempt number is even or odd.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

I'd explain it like this: every time you click a button or type something
in a Streamlit app, Streamlit doesn't just update that one part of the page
— it reruns your entire Python script from top to bottom, like refreshing
the page and re-executing everything. Normally that would mean all your
variables reset every single time, which would make it impossible to keep
track of things like a secret number or a running score across guesses.
That's what "session state" (st.session_state) is for — it's a dictionary
that survives across reruns for the same user session, so you can store
values in it once and they'll still be there the next time the script runs.
Working through this project's bugs made that click for me, because I saw
firsthand how easy it is to accidentally reset one piece of session state
(like attempts) while forgetting to reset another (like status), which is
exactly what caused the New Game soft-lock bug.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
- This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to keep is verifying fixes at the lowest level possible
before trusting them — instead of only testing through the full app in the
browser, I learned to run something like "python3 -c" to call the actual
function directly, which cut through a confusing situation where a stale
server process was hiding whether my fix actually worked. I also want to
keep committing in small, separate, clearly-labeled steps (FIXME comments,
then the fix, then tests, then documentation) instead of one giant commit
at the end, since it made it much easier to see what changed and why. One
thing I'd do differently next time is ask the AI to look at my actual
source code earlier, rather than letting it reason from a description or
memory of the code first — its first theory about the hint bug turned out
to be based on guessing and was more complicated than the real bug. This
project changed how I think about AI-generated code because it showed me
that AI output, whether from the assistant helping me or from the
originally "AI-generated" buggy game itself, can look completely confident
and reasonable while still being wrong, so checking it against real
behavior and real output is not optional.
