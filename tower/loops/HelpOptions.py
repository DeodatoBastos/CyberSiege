import pygame
from .GameLoop import GameLoop
from tower.constants import *
from tower.states import GameState
from tower.button import Button
from tower.resources import get_font
from dataclasses import dataclass

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_first_page = True
                game.set_state(GameState.main_menu)
                self.state = GameState.main_menu
            if event.key == pygame.K_LEFT:
                self.is_first_page = True
            if event.key == pygame.K_RIGHT:
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
