import pygame
from .GameLoop import GameLoop
from tower.constants import *
from tower.states import GameState
from tower.button import Button
from tower.resources import get_font
from dataclasses import dataclass
from .GamePlaying import GamePlaying

@dataclass
class GameEndedMenu(GameLoop):
    """
    Handle with game menu loop
    """
    play_button: Button
    quit_button: Button

    @classmethod
    def create(cls, screen, state):
        game_menu = cls(
            screen = screen,
            state = state,
            play_button = Button(image=None, pos=(480, 320), text_input="Play Again",
                                 font=get_font(60), base_color="#d7fcd4", 
                                 hovering_color="Green"),
            quit_button = Button(image=None, pos=(480, 420), text_input="Quit",
                                 font=get_font(60), base_color="#d7fcd4",
                                 hovering_color="Green")
        )
        return game_menu


    def loop(self, game, has_won):
        if has_won:
            title_texts = ["Well done!", "You're a cybersecurity pro!"]
        else:
            title_texts = ["You've been hacked!"]

        self.state = game.state
        clock = pygame.time.Clock()
        self.screen.blit(IMAGE_SPRITES[(False, False, "menu")], (0, 0))
        menu_texts = [get_font(35).render(title_text, True, "#b68f40") for title_text in title_texts]
        menu_rect = menu_texts[0].get_rect(center=(480, 50))

        for i, menu_text in enumerate(menu_texts):
                self.screen.blit(menu_text, (menu_rect[0] - 290 * i, menu_rect[1] + 40 * i))

        while self.state == GameState.game_ended:
            mouse_pos = pygame.mouse.get_pos()

            self.handle_events(game)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)
            mouse_pos = pygame.mouse.get_pos()

            for button in [self.play_button, self.quit_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)


    def handle_event(self, event, game):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.checkForInput(mouse_pos):
                game.set_state(GameState.game_playing)
                game.game_playing = GamePlaying.create(self.screen, GameState.game_playing)
                self.state = GameState.game_playing
            if self.quit_button.checkForInput(mouse_pos):
                game.set_state(GameState.quitting)
                self.state = GameState.quitting

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.set_state(GameState.quitting)
                self.state = GameState.quitting
            if event.key == pygame.K_p:
                game.set_state(GameState.game_playing)
                game.game_playing = GamePlaying.create(self.screen, GameState.game_playing)
                self.state = GameState.game_playing
            if event.key == pygame.K_q:
                game.set_state(GameState.quitting)
                self.state = GameState.quitting
