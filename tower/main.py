# Local imports
from dataclasses import dataclass
from tower.constants import *
from tower.states import GameState, StateError

# External imports
import pygame


@dataclass
class TowerGame:

    screen: pygame.Surface
    screen_rect: pygame.Rect
    fullscreen: bool
    state: GameState

    @classmethod
    def create(cls, fullsc=False):
        game = cls(
            screen=None,
            screen_rect=SCREENRECT,
            fullscreen=fullsc,
            state=GameState.initializing
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

        #Initializing sprites
        allSprites = pygame.sprite.Group()
        tile = TileSprite()
        allSprites.add(tile)
        self.loop(allSprites)
        print(allSprites)

    def loop(self,all_sprites):
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

            #Rendering and updating sprites
            all_sprites.update()
            clock.tick(DESIRED_FPS)
            all_sprites.draw(self.screen)
            pygame.display.flip()
            
            #FPS
            clock.tick(DESIRED_FPS)
        self.quit()

    def quit(self):
        pygame.quit()

    def init(self):
        self.assert_state_is(GameState.initializing)
        pygame.init()
        window_style = pygame.RESIZABLE #pygame.FULLSCREEN if self.fullscreen else 0
        # We want 32 bits of color depth
        bit_depth = pygame.display.mode_ok(self.screen_rect.size, window_style, 32)
        screen = pygame.display.set_mode(self.screen_rect.size, window_style, bit_depth)
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

class TileSprite(pygame.sprite.Sprite):
    def __init__(self):
        #Image, rect are attributes
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(pygame.Color(0,255,0,255))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 200)

game = TowerGame.create(TowerGame)
game.start_game()
