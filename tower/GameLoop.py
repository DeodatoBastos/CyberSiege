from dataclasses import dataclass
import pygame
from tower.constants import *
from tower.states import GameState
from tower.button import Button
from tower.resources import get_font

@dataclass
class GameLoop:
    screen: pygame.Surface
    state: GameState

    def handle_events(self, game):
        """
        Sample event handler that ensures quit events and normal
        event loop processing takes place. Without this, the game will
        hang, and repaints by the operating system will not happen,
        causing the game window to hang.
        """
        for event in pygame.event.get():
            if (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ) or event.type == pygame.QUIT:
                game.set_state(GameState.quitting)
                self.state = GameState.quitting

            # Delegate the event to a sub-event handler `handle_event`
            self.handle_event(event, game)


    def loop(self, game):
        while self.state != GameState.quitting:
            self.handle_events(game)


    def handle_event(self, event, game):
        """
        Handles a singular event, `event`.
        """


@dataclass
class GameMenu(GameLoop):
    play_button: Button
    help_button: Button
    quit_button: Button

    @classmethod
    def create(cls, screen, state):
        game_menu = cls(
            screen = screen,
            state = state,
            play_button = Button(image=None, pos=(480, 320), 
                            text_input="Play", font=get_font(60), base_color="#d7fcd4",
                            hovering_color="Green"),
            help_button = Button(image=None, pos=(480, 420), 
                            text_input="Help", font=get_font(60), base_color="#d7fcd4",
                            hovering_color="Green"),
            quit_button = Button(image=None, pos=(480, 520), 
                            text_input="Quit", font=get_font(60), base_color="#d7fcd4",
                            hovering_color="Green")
        )
        return game_menu


    def loop(self, game):
        clock = pygame.time.Clock()
        self.screen.blit(IMAGE_SPRITES[(False, False, "menu")], (0, 0))

        MENU_TEXT = get_font(80).render("Cyber Siege", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(480, 100))
        self.screen.blit(MENU_TEXT, MENU_RECT)

        while self.state == GameState.main_menu:
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            self.handle_events(game)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)

            for button in [self.play_button, self.help_button, self.quit_button]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)


    def handle_event(self, event, game):
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.checkForInput(MENU_MOUSE_POS):
                game.set_state(GameState.game_playing)
                self.state = GameState.game_playing
            if self.help_button.checkForInput(MENU_MOUSE_POS):
                game.set_state(GameState.help_options)
                self.state = GameState.help_options
            if self.quit_button.checkForInput(MENU_MOUSE_POS):
                game.set_state(GameState.quitting)
                self.state = GameState.quitting


class GameEditing(GameLoop):
    pass


class GamePlaying(GameLoop):
     def loop(self, game):
        clock = pygame.time.Clock()
        self.screen.blit(IMAGE_SPRITES[(False, False, "map01")], (0, 0))
        while self.state == GameState.game_playing:
            self.handle_events(game)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)


class HelpOptions(GameLoop):
     def loop(self, game):
        clock = pygame.time.Clock()
        self.screen.fill("black")
        PLAY_TEXT = get_font(25).render("This is the Help screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(480, 260))
        self.screen.blit(PLAY_TEXT, PLAY_RECT)

        while self.state == GameState.help_options:
            self.handle_events(game)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)
