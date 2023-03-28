from dataclasses import dataclass
import pygame
from tower.constants import *
from tower.states import GameState
from tower.enemies.sql_injection import Sql_Injection

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
            self.handle_event(event)


    def loop(self, game):
        while self.state != GameState.quitting:
            self.handle_events(game)

    def handle_event(self, event):
        """
        Handles a singular event, `event`.
        """


class GameMenu(GameLoop):
    def loop(self, game):
        self.state = game.state
        clock = pygame.time.Clock()
        sql = Sql_Injection()
        while self.state == GameState.main_menu:
            self.handle_events(game)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            self.screen.blit(IMAGE_SPRITES[(False, False, "background")], (0, 0))
            sql.draw(game.screen)
            sql.draw_health_bar(game.screen)
            sql.move()
            clock.tick(DESIRED_FPS)


class GameEditing(GameLoop):
    pass
