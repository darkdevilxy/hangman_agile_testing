import random
import threading
import time

# Lists to store words and phrases for the game
words = []
phrases = []

# Game states
MENU = "menu"
GAME = "game"
GAMEOVER = "gameover"

# Game variables
life_remaining = 6
guessed_letters = []
wrong_letters = []
mistakes = 0
current_word = ""
word_state = []
timeout = 0

timer = None


def setup(mode):
    """
    Initializes the game based on the selected mode.
    Sets up the timer and chooses a word or phrase.
    """
    global current_word
    global word_state

    start_timer(15)

    if mode == "basic":
        current_word = choose_word()
    elif mode == "intermediate":
        current_word = choose_phrase()
    print(current_word)

    # Initialize word_state with underscores
    if word_state == []:
        for i in current_word:
            if i == " ":
                word_state.append(" ")
            else:
                word_state.append("_")


def choose_word() -> str:
    """
    Chooses a random word from the dataset.
    Loads words from file if not already loaded.
    """
    if words == []:
        with open("./datasets/cleaned_data.txt", "r") as f:
            for data in f:
                words.append(data.strip())
    random_number = random.randrange(0, len(words))
    return words[random_number]


def choose_phrase() -> str:
    """
    Chooses a random phrase from the dataset.
    Loads phrases from file if not already loaded.
    """
    if phrases == []:
        with open("./datasets/phrases.txt", "r") as f:
            for data in f:
                phrases.append(data.strip())
    random_number = random.randrange(0, len(phrases))
    return phrases[random_number]


def guess_letters(letter):
    """
    Handles guessing a letter.
    Updates guessed letters, word state, and life remaining.
    Resets the timer on each guess.
    """
    global word_state
    global guessed_letters
    global life_remaining

    reset_timer(15)

    word_state = []

    guessed_letters.append(letter)

    # If guessed letter is not in the word, reduce life
    if letter not in current_word.upper():
        life_remaining -= 1

    # Update word_state with guessed letters
    for i in current_word.upper():
        if i in guessed_letters:
            word_state.append(i)
        elif i == " ":
            word_state.append(" ")
        else:
            word_state.append("_")


def reduce_life():
    """
    Reduces the player's remaining lives by one.
    """
    global life_remaining
    life_remaining -= 1


def start_timer(seconds):
    """
    Starts the countdown timer for the game.
    Cancels any existing timer before starting a new one.
    """
    global timer, timeout

    if timer:
        timer.cancel()
    timeout = seconds
    countdown()


def countdown():
    """
    Handles the countdown logic.
    Reduces timeout every second and reduces life when time runs out.
    """
    global timer, timeout

    timeout -= 1
    if timeout >= 1:
        timer = threading.Timer(1.0, countdown)
        timer.start()
    else:
        reduce_life()


def game_over():
    """
    Resets all game variables to their initial state.
    """
    global timeout, guessed_letters, mistakes, current_word, word_state, life_remaining

    timeout = 0
    guessed_letters = []
    mistakes = 0
    current_word = ""
    word_state = []
    life_remaining = 6


def reset_timer(seconds):
    """
    Resets the countdown timer to the specified number of seconds.
    """
    start_timer(seconds)
