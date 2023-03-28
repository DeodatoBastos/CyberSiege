from dataclasses import dataclass
import pygame
from tower.constants import *
from tower.states import GameState

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
        self.screen.blit(IMAGE_SPRITES[(False, False, "background")], (0, 0))
        while self.state == GameState.main_menu:
            self.handle_events(game)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)


class GameEditing(GameLoop):
    pass

#Ctrl
from tower.GUI import button
class MainGame(GameLoop):
    def loop(self, game):
        self.state = game.state
        clock = pygame.time.Clock()
        self.screen.blit(IMAGE_SPRITES[(False, False, "background")], (0, 0))

        #Defining the buttons (tower selection)
        antivirus_button = button((0,255,0),150,150,100,50,'antivirus')
        allButtons = [antivirus_button]

        while self.state == GameState.game_playing:
            self.handle_events(game)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)

            #Renderização dos buttons
            for b in allButtons:
                b.draw(self.screen,(0,0,0))