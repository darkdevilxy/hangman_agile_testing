import pygame
import string
import core
import components

pygame.init()

# Screen setup
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hangman Game with Letter Selection")

# Font for button text
font = pygame.font.Font("./assets/font.ttf", 18)
font_medium = pygame.font.Font("./assets/font.ttf", 24)
font_large = pygame.font.Font("./assets/font.ttf", 30)

class Game:
    def __init__(self):
        # Initial game state (menu, game, gameover)
        self.state = core.MENU
        self.mode = None  # Game mode (basic/intermediate)
        # Load letter spritesheet for letter buttons
        self.letter_sheet = components.ScrabbleLetterSheet(
            "./assets/letters.png"
        )
        # Load hangman spritesheet for hangman drawing
        self.hangman_sprites = components.HangmanSprites(
            "./assets/hangman_sheet.png"
        )
        # Group to hold letter button sprites
        self.letter_buttons = pygame.sprite.Group()
        # Timer for transitions (not used for animation here)
        self.transition_timer = 0
        # Track mistakes, word state, lives, and timeout from core logic
        self.mistakes = core.mistakes
        self.word_state = core.word_state
        self.life_remaining = core.life_remaining
        self.timeout = str(core.timeout)
        # Menu buttons for selecting game mode
        self.basic_button = components.Button(
            "./assets/button.svg",
            "./assets/button_clicked.svg",
            (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2),
            "Basic",
            font,
        )
        self.intermediate_button = components.Button(
            "./assets/button.svg",
            "./assets/button_clicked.svg",
            (SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2),
            "Intermediate",
            font,
        )
        # Underscores for displaying current word state
        self.underscores = components.Underscores(self.word_state, font)
        # Game over screen component
        self.gameover = components.GameOverScreen(
            font_large, font, SCREEN_HEIGHT, SCREEN_WIDTH
        )

    def create_letter_buttons(self):
        """Create clickable letter buttons for A-Z and arrange them in a grid on the right side."""
        self.letter_buttons.empty()
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Grid positioning variables
        start_x = SCREEN_WIDTH - 400
        start_y = 120
        cols = 5
        spacing_x = 70
        spacing_y = 70

        for i, letter in enumerate(letters):
            col = i % cols
            row = i // cols

            x = start_x + (col * spacing_x)
            y = start_y + (row * spacing_y)

            # Get letter image from spritesheet
            letter_surface = self.letter_sheet.get_letter(letter)
            if letter_surface:
                # Create button sprite and add to group
                letter_button = components.LetterButton(letter_surface, (x, y), letter)
                self.letter_buttons.add(letter_button)

    def handle_events(self, event):
        """Handle all pygame events (mouse, keyboard) depending on game state."""
        if self.state == core.MENU:
            # Handle menu button clicks
            if self.basic_button.handle_event(event):
                print("Basic Mode")
                core.setup("basic")  # Setup game logic for basic mode
                self.state = core.GAME
                self.create_letter_buttons()
                self.transition_timer = 0

            if self.intermediate_button.handle_event(event):
                print("Intermediate Mode")
                core.setup("intermediate")  # Setup game logic for intermediate mode
                self.state = core.GAME
                self.create_letter_buttons()
                self.transition_timer = 0

        elif self.state == core.GAME:
            # Handle letter button clicks
            for button in self.letter_buttons:
                clicked_letter = button.handle_event(event)
                if clicked_letter:
                    core.guess_letters(clicked_letter)  # Update game logic with guessed letter
                    self.word_state = core.word_state
                    self.life_remaining = core.life_remaining
                    if "_" not in self.word_state and self.life_remaining > 0:
                        core.game_over()
                        self.state = core.MENU
                        self.letter_buttons.empty()
                        self.mistakes = 0
                        core.life_remaining = 6

                    # If no lives left, trigger game over
                    if self.life_remaining <= 0:
                        core.game_over()
                        self.state = core.GAMEOVER

        # Handle escape key to return to menu (works in any state)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            core.game_over()
            self.state = core.MENU
            self.letter_buttons.empty()
            self.mistakes = 0
            core.life_remaining = 6

    def update(self):
        """Update game state and components each frame."""
        if self.state == core.MENU:
            self.basic_button.update()
            self.intermediate_button.update()
        elif self.state == core.GAME:
            # Sync word state and update letter buttons
            self.word_state = core.word_state
            self.letter_buttons.update()
            self.transition_timer += 1
            # Calculate mistakes from lives
            self.mistakes = 6 - core.life_remaining
            self.timeout = str(core.timeout)
            # Update underscores display
            self.underscores = components.Underscores(self.word_state, font)

    def draw(self, surface):
        """Draw all game elements to the screen depending on state."""
        surface.fill((30, 30, 50))  # Dark blue background

        if self.state == core.MENU:
            # Draw menu buttons
            self.basic_button.draw(surface)
            self.intermediate_button.draw(surface)

            # Draw title
            title_font = pygame.font.Font(None, 48)
            title_text = title_font.render("HANGMAN GAME", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            surface.blit(title_text, title_rect)

            # Draw instructions
            instruction_text = font.render(
                "Click Basic or Intermediate to start", True, (255, 255, 255)
            )
            text_rect = instruction_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
            )
            surface.blit(instruction_text, text_rect)
        elif self.state == core.GAMEOVER:
            # Draw game over screen
            self.gameover.draw(screen)

        elif self.state == core.GAME:
            # Draw underscores for word state
            self.underscores.draw_underscores(surface)
            # Draw hangman sprite based on mistakes
            hangman_frame = self.hangman_sprites.get_frame(self.mistakes)
            if hangman_frame:
                hangman_rect = hangman_frame.get_rect()
                hangman_rect.center = (250, SCREEN_HEIGHT // 2)
                surface.blit(hangman_frame, hangman_rect)

            # Draw game info (mode, lives, mistakes, timer)
            mode_text = pygame.font.Font(None, 24).render(
                f"Mode: {self.mode}", True, (255, 255, 255)
            )
            surface.blit(mode_text, (20, 20))

            lives_text = pygame.font.Font(None, 24).render(
                f"Lives: {core.life_remaining}", True, (255, 100, 100)
            )
            surface.blit(lives_text, (20, 50))

            mistakes_text = pygame.font.Font(None, 20).render(
                f"Mistakes: {self.mistakes}/6", True, (255, 200, 100)
            )
            surface.blit(mistakes_text, (20, 80))
            count_down_text = pygame.font.Font("./assets/font.ttf", 20).render(
                self.timeout, True, "white"
            )
            surface.blit(count_down_text, (20, 110))

            # Draw instructions
            instruction_text = pygame.font.Font(None, 18).render(
                "Press ESC to return to menu", True, (200, 200, 200)
            )
            surface.blit(instruction_text, (20, SCREEN_HEIGHT - 30))

            # Draw all letter buttons
            self.letter_buttons.draw(surface)

# Initialize game instance
game = Game()
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            core.timer.cancel()  # Cancel any running timer in core logic

        game.handle_events(event)  # Pass event to game

    game.update()  # Update game state
    game.draw(screen)  # Draw everything
    pygame.display.flip()  # Update display
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
