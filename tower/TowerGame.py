# Local imports
from dataclasses import dataclass, field
from tower.constants import *
from tower.states import GameState, StateError
from tower.resources import *
from tower.GameLoop import *

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
    game_menu: GameLoop = field(init=False, default=None)
    game_playing: GameLoop = field(init=False, default=None)
    game_play: GameLoop = field(init=False, default=None)
    help_options: GameLoop = field(init=False, default=None)

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
        self.loop()

    def loop(self):
        while self.state != GameState.quitting:

            if self.state == GameState.main_menu:
                self.game_menu.loop(game=self)

            elif self.state == GameState.map_editing:
                pass

            elif self.state == GameState.game_playing:
                self.game_play.loop(game=self)
                self.game_playing.loop(game=self)
            elif self.state == GameState.help_options:
                self.help_options.loop(game=self)

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

        #initializing sprites
        for sprite_index, sprite_name in SPRITES.items():
            img = import_image(sprite_name)
            for flipped_x in (True, False):
                for flipped_y in (True, False):
                    new_img = pygame.transform.flip(img, flip_x=flipped_x, flip_y=flipped_y)
                    IMAGE_SPRITES[(flipped_x, flipped_y, sprite_index)] = new_img

        # initializing audio
        for channel_id, channel_name in enumerate(channels):
            channels[channel_name] = pygame.mixer.Channel(channel_id)
            # Configure the volume here.
            channels[channel_name].set_volume(1.0)

        self.game_play = MainGame(screen=self.screen, state=self.state)
        self.game_menu = GameMenu.create(self.screen, GameState.main_menu)
        self.game_playing = GamePlaying(screen=self.screen, state=GameState.game_playing)
        self.help_options = HelpOptions.create(self.screen, GameState.help_options)
        self.set_state(GameState.initialized)
