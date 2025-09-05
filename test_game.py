import unittest
import time
import core  # assume your code is saved in core.py


# Test suite for the core Hangman game logic
class TestWordcore(unittest.TestCase):

    def setUp(self):
        # Set up test data and reset game state before each test
        core.words = ["python", "hangman", "test"]
        core.phrases = ["machine learning", "data science"]
        core.game_over()  # reset state before each test

    def test_choose_word(self):
        # Test that choose_word returns a word from the list
        word = core.choose_word()
        self.assertIn(word, core.words)

    def test_choose_phrase(self):
        # Test that choose_phrase returns a phrase from the list
        phrase = core.choose_phrase()
        self.assertIn(phrase, core.phrases)

    def test_setup_basic(self):
        # Test basic setup initializes word and state correctly
        core.setup("basic")
        self.assertIn(core.current_word, core.words)
        self.assertEqual(len(core.word_state), len(core.current_word))
        self.assertTrue(all(ch == "_" for ch in core.word_state))

    def test_setup_intermediate(self):
        # Test intermediate setup initializes phrase and state correctly
        core.setup("intermediate")
        self.assertIn(core.current_word, core.phrases)
        self.assertEqual(len(core.word_state), len(core.current_word))
        # Spaces in the phrase should be revealed immediately.
        for i, ch in enumerate(core.current_word):
            if ch == " ":
                self.assertEqual(
                    core.word_state[i], " "
                )  # Expecting a space, not an underscore
            else:
                self.assertEqual(
                    core.word_state[i], "_"
                )  # All other characters are underscores

    def test_guess_correct_letter(self):
        # Test guessing a correct letter updates word_state
        core.current_word = "PYTHON"
        core.word_state = ["_", "_", "_", "_", "_", "_"]
        core.guessed_letters = []
        core.guess_letters("P")
        self.assertIn("P", core.word_state)

    def test_guess_wrong_letter(self):
        # Test guessing a wrong letter reduces life_remaining
        core.current_word = "PYTHON"
        core.word_state = ["_", "_", "_", "_", "_", "_"]
        core.life_remaining = 6
        core.guessed_letters = []
        core.guess_letters("Z")
        self.assertEqual(core.life_remaining, 5)

    def test_timer_reduces_life(self):
        # Test timer expiration reduces life_remaining
        core.life_remaining = 6
        core.start_timer(1)  # short timer for test
        time.sleep(2)  # wait until timer expires
        self.assertEqual(core.life_remaining, 5)

    def test_reset_core(self):
        # Test game_over resets all game state variables
        core.current_word = "PYTHON"
        core.life_remaining = 3
        core.word_state = ["P", "_", "_"]
        core.guessed_letters = ["P"]
        core.game_over()
        self.assertEqual(core.life_remaining, 6)
        self.assertEqual(core.current_word, "")
        self.assertEqual(core.word_state, [])
        self.assertEqual(core.guessed_letters, [])

    def test_win_condition(self):
        #word_state matches current_word
        core.current_word = "TEST"
        core.word_state = list("TEST")
        self.assertNotIn("_", core.word_state)
        self.assertEqual("".join(core.word_state), core.current_word)

    def test_loss_condition(self):
        # life_remaining is zero and word_state has underscores
        core.current_word = "TEST"
        core.word_state = ["_", "_", "_", "_"]
        core.life_remaining = 0
        self.assertEqual(core.life_remaining, 0)
        self.assertIn("_", core.word_state)


if __name__ == "__main__":
    unittest.main()
