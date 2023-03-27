# Local imports
from dataclasses import dataclass
from tower.constants import *
from tower.states import GameState, StateError
from tower.sprites import TileSprite


# External imports
import pygame
from pygame.locals import *
import os


@dataclass
class TowerGame:

    screen: pygame.Surface
    screen_rect: pygame.Rect
    fullscreen: bool
    state: GameState
    background: pygame.image

    @classmethod
    def create(cls, fullsc=False):
        game = cls(
            screen=None,
            screen_rect=SCREENRECT,
            fullscreen=fullsc,
            state=GameState.initializing,
            background=pygame.image.load(os.path.join(
                "tower", "assets", "sprites", "map01.png"))
        )
        game.init()
        return game

    def set_state(self, new_state):
        self.state = new_state

    def assert_state_is(self, *expected_states: GameState):
        """
        Asserts that the game engine is one of
        `expected_states`. If that assertions fails, raise
        `StateError`.
        """
        if not self.state in expected_states:
            raise StateError(
                f"Expected the game state to be one of {expected_states} not {self.state}"
            )

    def start_game(self):
        self.assert_state_is(GameState.initialized)
        self.set_state(GameState.main_menu)

        # Initializing sprites
        allSprites = pygame.sprite.Group()
        tile = TileSprite()
        allSprites.add(tile)
        self.loop(allSprites)
        print(allSprites)

    def loop(self, all_sprites):
        clock = pygame.time.Clock()
        while self.state != GameState.quitting:
            if self.state == GameState.main_menu:
                # pass control to the game menu's loop
                pass
            elif self.state == GameState.map_editing:
                # ... etc ...
                pass
            elif self.state == GameState.game_playing:
                # ... etc ...
                pass

            # Rendering and updating sprites
            all_sprites.update()
            clock.tick(DESIRED_FPS)
            all_sprites.draw(self.screen)
            pygame.display.flip()

            # Background render
            self.screen.blit(self.background, (0, 0))
            # FPS
            clock.tick(DESIRED_FPS)
        self.quit()

    def quit(self):
        pygame.quit()

    def init(self):
        self.assert_state_is(GameState.initializing)
        pygame.init()
        window_style = pygame.RESIZABLE  # pygame.FULLSCREEN if self.fullscreen else 0
        bit_depth = pygame.display.mode_ok(
            self.screen_rect.size, window_style, 32)
        screen = pygame.display.set_mode(
            self.screen_rect.size, window_style, bit_depth)
        pygame.mixer.pre_init(
            frequency=44100,
            size=32,
            # N.B.: 2 here means stereo, not the number of channels to
            # use in the mixer
            channels=2,
            buffer=512,
        )
        pygame.font.init()
        self.screen = screen
        self.set_state(GameState.initialized)
