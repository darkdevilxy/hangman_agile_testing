import pygame
import string

def test_setup_intermediate(self):
        # Test intermediate setup initializes phrase and state correctly
        core.setup("intermediate")
        self.assertIn(core.current_word, core.phrases)
        self.assertEqual(len(core.word_state), len(core.current_word))
        # Spaces in the phrase should be revealed immediately.
        for i, ch in enumerate(core.current_word):
            if ch == " ":
                self.assertEqual(core.word_state[i], " ")  # Expecting a space, not an underscore
            else:
                self.assertEqual(core.word_state[i], "_") # All other characters are underscores

# Button class for clickable UI buttons
class Button(pygame.sprite.Sprite):
    def __init__(self, normal_img, clicked_img, pos, text, font):
        super().__init__()
        # Load button images for normal and clicked states
        self.normal_img = pygame.image.load(normal_img).convert_alpha()
        self.clicked_img = pygame.image.load(clicked_img).convert_alpha()

        self.image = self.normal_img
        self.rect = self.image.get_rect(center=pos)
        self.font = font

        # Render button text
        self.text_surf = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.clicked = False

    def update(self):
        # Update button image based on clicked state
        self.image = self.clicked_img if self.clicked else self.normal_img
        self.text_rect.center = self.rect.center

    def handle_event(self, event):
        # Handle mouse events for button interaction
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                return True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False
        return False

    def draw(self, surface):
        # Draw button and text on the given surface
        surface.blit(self.image, self.rect)
        surface.blit(self.text_surf, self.text_rect)

# LetterButton class for clickable letter tiles
class LetterButton(pygame.sprite.Sprite):
    def __init__(self, letter_surface, pos, letter):
        super().__init__()
        self.letter = letter
        self.original_image = letter_surface.copy()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.clicked = False
        self.disabled = False
        self.alpha = 0  # For fade-in effect

    def update(self):
        # Fade in effect for letter button
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + 8)

        # Create image based on state
        self.image = self.original_image.copy()

        if self.disabled:
            # Gray out disabled letters
            self.image.fill((100, 100, 100), special_flags=pygame.BLEND_MULT)

        self.image.set_alpha(self.alpha)

    def handle_event(self, event):
        # Handle mouse events for letter button interaction
        if self.disabled:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                self.disabled = True
                return self.letter
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False
        return None

# Loads Scrabble-style letter tiles from a spritesheet
class ScrabbleLetterSheet:
    def __init__(self, spritesheet_path):
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        self.letters = {}
        self.load_letters_from_scrabble_sheet()

    def load_letters_from_scrabble_sheet(self):
        """Load letters from the Scrabble-style spritesheet"""
        # Assuming your spritesheet has 8 columns and 4 rows (26 letters + 6 empty spaces)
        tile_width = self.spritesheet.get_width() // 8
        tile_height = self.spritesheet.get_height() // 4

        alphabet = string.ascii_uppercase

        for i, letter in enumerate(alphabet):
            col = i % 8
            row = i // 8

            x = col * tile_width
            y = row * tile_height

            # Extract letter tile from spritesheet
            letter_surface = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
            letter_surface.blit(
                self.spritesheet, (0, 0), (x, y, tile_width, tile_height)
            )

            self.letters[letter] = letter_surface

    def get_letter(self, letter):
        # Get the surface for a specific letter
        return self.letters.get(letter.upper())

# Loads hangman frames from a spritesheet for animation
class HangmanSprites:
    def __init__(self, spritesheet_path):
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        self.frames = []
        self.load_hangman_frames()

    def load_hangman_frames(self):
        """Load hangman frames from spritesheet"""
        # Assuming 4 columns, 2 rows for 8 frames
        frame_width = self.spritesheet.get_width() // 4
        frame_height = self.spritesheet.get_height() // 2

        for i in range(8):
            col = i % 4
            row = i // 4

            x = col * frame_width
            y = row * frame_height

            # Extract frame from spritesheet
            frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surface.blit(
                self.spritesheet, (0, 0), (x, y, frame_width, frame_height)
            )

            self.frames.append(frame_surface)

    def get_frame(self, mistakes):
        """Get hangman frame based on number of mistakes (0-7)"""
        frame_index = min(mistakes, len(self.frames) - 1)
        return self.frames[frame_index] if self.frames else None

# Draws underscores and revealed letters for the word
class Underscores: 
    def __init__(self, word, font) -> None:
        self.word = word
        self.font = font
        self.spacing = 30  # Space between letters

    def draw_underscores(self, surface):
        # Draw underscores and revealed letters on the surface
        i = 1
        for letter in self.word:
            text_surface = self.font.render(letter, True, (255, 255, 255))
            text_rectangle = text_surface.get_rect(center=(350 + i * self.spacing, 600))
            surface.blit(text_surface, text_rectangle)
            i += 1

# Displays the game over screen
class GameOverScreen:
    def __init__(self, font_large, font, SCREEN_HEIGHT, SCREEN_WIDTH) -> None:
        self.game_over_text = font_large.render("Game Over!", True, "white")
        self.press_key_text = font.render("Press ESC to jump to main menu", True, "white")

        # Get the rectangular areas of the rendered text to position them.
        self.game_over_rect = self.game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.press_key_rect = self.press_key_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    
    def draw(self, screen):
        # Draw game over messages on the screen
        screen.blit(self.game_over_text, self.game_over_rect)
        screen.blit(self.press_key_text, self.press_key_rect)

# Displays a countdown message
class Countdown:
    def __init__(self, font, text) -> None:
        self.count_down_text = font.render(text, True, "white")
        self.count_down_text_rect = self.count_down_text.get_rect(center=(300, 300))
    def draw(self, screen):
        # Draw countdown text on the screen
        screen.blit(self.count_down_text, self.count_down_text_rect)