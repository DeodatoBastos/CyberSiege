from tower.constants import *
from tower.states import GameState
from tower.enemies.sql_injection import Sql_Injection
from tower.button import Button
from tower.resources import get_font
from tower.GUI import button

from dataclasses import dataclass
import pygame


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
    """
    Handle with game menu loop
    """
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
        self.state = game.state
        clock = pygame.time.Clock()
        self.screen.blit(IMAGE_SPRITES[(False, False, "menu")], (0, 0))
        menu_text = get_font(80).render("Cyber Siege", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(480, 100))
        self.screen.blit(menu_text, menu_rect)

        while self.state == GameState.main_menu:
            mouse_pos = pygame.mouse.get_pos()

            self.handle_events(game)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)
            mouse_pos = pygame.mouse.get_pos()

            for button in [self.play_button, self.help_button, self.quit_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)


    def handle_event(self, event, game):
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.checkForInput(mouse_pos):
                game.set_state(GameState.game_playing)
                self.state = GameState.game_playing
            if self.help_button.checkForInput(mouse_pos):
                game.set_state(GameState.help_options)
                self.state = GameState.help_options
            if self.quit_button.checkForInput(mouse_pos):
                game.set_state(GameState.quitting)
                self.state = GameState.quitting


class GameEditing(GameLoop):
    pass


class GamePlaying(GameLoop):
    """
    Handle with playing loop
    """
    def loop(self, game):
        self.state = game.state
        clock = pygame.time.Clock()
        sql = Sql_Injection()

        #Defining the buttons (tower selection)
        antivirus_button = button((0, 255, 0), 150, 150, 100, 50, 'antivirus')
        allButtons = [antivirus_button]

        while self.state == GameState.game_playing:
            self.handle_events(game)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            self.screen.blit(IMAGE_SPRITES[(False, False, "map01")], (0, 0))
            sql.draw(game.screen)
            sql.draw_health_bar(game.screen)
            sql.move()
            clock.tick(DESIRED_FPS)

            #render all buttons
            for btn in allButtons:
                btn.draw(self.screen,(0,0,0))



@dataclass
class HelpOptions(GameLoop):
    """
    Handle with help options menu
    """
    back_menu_button: Button
    back_page_button: Button
    forward_page_button: Button
    is_first_page: bool

    @classmethod
    def create(cls, screen, state):
        help_options = cls(
            screen = screen,
            state = state,
            back_menu_button = Button(image=None, pos=(80, 600), 
                            text_input="Back", font=get_font(25), base_color="White",
                            hovering_color="Green"),
            back_page_button = Button(image=None, pos=(420, 600), 
                            text_input="<", font=get_font(30), base_color="White",
                            hovering_color="Green"),
            forward_page_button = Button(image=None, pos=(540, 600), 
                            text_input=">", font=get_font(30), base_color="White",
                            hovering_color="Green"),
            is_first_page = True
        )
        return help_options


    def loop(self, game):
        self.state = game.state
        clock = pygame.time.Clock()

        while self.state == GameState.help_options:
            self.handle_events(game)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)

            if self.is_first_page:
                self.draw_first_page()
            else:
                self.draw_second_page()


    def handle_event(self, event, game):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_menu_button.checkForInput(mouse_pos):
                self.is_first_page = True
                game.set_state(GameState.main_menu)
                self.state = GameState.main_menu
            if self.back_page_button.checkForInput(mouse_pos):
                self.is_first_page = True
            if self.forward_page_button.checkForInput(mouse_pos):
                self.is_first_page = False


    def draw_first_page(self):
        self.screen.fill("black")
        help_text = get_font(25).render("This is the first Help screen.", True, "White")
        help_rect = help_text.get_rect(center=(480, 260))
        number_page = get_font(30).render(" 1/2 ", True, "White")
        number_page_rect = number_page.get_rect(center=(480, 600))
        self.screen.blit(number_page, number_page_rect)
        self.screen.blit(help_text, help_rect)
        self.update_buttons()


    def draw_second_page(self):
        self.screen.fill("black")
        help_text = get_font(25).render("This is the second Help screen.", True, "White")
        help_rect = help_text.get_rect(center=(480, 260))
        self.screen.blit(help_text, help_rect)
        number_page = get_font(30).render(" 2/2 ", True, "White")
        number_page_rect = number_page.get_rect(center=(480, 600))
        self.screen.blit(number_page, number_page_rect)
        self.update_buttons()


    def update_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        
        self.back_menu_button.changeColor(mouse_pos)
        self.back_menu_button.update(self.screen)

        self.back_page_button.changeColor(mouse_pos)
        self.back_page_button.update(self.screen)

        self.forward_page_button.changeColor(mouse_pos)
        self.forward_page_button.update(self.screen)
