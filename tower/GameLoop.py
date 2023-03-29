from tower.constants import *
from tower.states import GameState
from tower.enemies.sql_injection import Sql_Injection
from tower.button import Button
from tower.resources import get_font
from tower.towers import antivirus, firewall, twoFactorAuth, Towers

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

@dataclass
class GamePlaying(GameLoop):

    antivirus_button : Button
    firewall_button: Button
    twoFA_button : Button
    allButtons : "list[Button]"
    allTowers : "list[Towers,(int,int)]"
    balance : int
    grabbing : bool
    grabbed : bool

    @classmethod
    def create(cls, screen, state):
        game_playing = cls(
            screen = screen,
            state = state,
            antivirus_button = Button(image=antivirus.img,pos=(896+33,64),text_input="",font=get_font(1),base_color="#d7fcd4", hovering_color="ffffff"),
            firewall_button = Button(image=firewall.img,pos=(896+33,160),text_input="",font=get_font(1),base_color="#d7fcd4", hovering_color="ffffff"),
            twoFA_button = Button(image=twoFactorAuth.img,pos=(896+33,258),text_input="",font=get_font(1),base_color="#d7fcd4", hovering_color="ffffff"),
            allButtons = [],
            allTowers = [],
            balance = 100,
            grabbing = False,
            grabbed = False
        )
        return game_playing

    def loop(self, game):
        self.state = game.state
        clock = pygame.time.Clock()

        sql = Sql_Injection()

        # Defining Tower templates for the buttons to reefer cause i dunno a better way to do it
        #av_template = antivirus()
        #firewall_template = firewall()
        #twoFA_template = twoFactorAuth()

        # Defining the buttons (tower selection)
        #antivirus_button = button(av_template, 896 + 5, 32, 64,64, 54,'')
        #firewall_button = button(firewall_template, 896 + 5, 128, 64,64, 54,'')
        #twoFA_button = button(twoFA_template, 896 + 5, 224, 64,64, 54,'')
        self.allButtons = [self.antivirus_button, self.firewall_button, self.twoFA_button]

        # Grabbing tower state

        # money
        #balance = 100

        while self.state == GameState.game_playing:
            self.handle_events(game)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            self.screen.blit(IMAGE_SPRITES[(False, False, "map01")], (0, 0))
            sql.draw(game.screen)
            sql.draw_health_bar(game.screen)
            sql.move()
            clock.tick(DESIRED_FPS)

            # Rendering the buttons
            for btn in self.allButtons:
                btn.update(self.screen)

            # Render deployed towers
            for element in self.allTowers:
                self.screen.blit(pygame.transform.scale(element[0].img, (32,32)), (element[1][0] - 16, element[1][1] - 16))

            # while grabbing something, render it at mouse position each frame
            if (self.grabbing):
                self.screen.blit(pygame.transform.scale(self.grabbed.img, (32,32)), (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))
                

    def handle_event(self, event, game):
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3):
            self.grabbing = False
            self.grabbed = None

        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.grabbing == False):
            # check if the user click in any button
            mousePos = pygame.mouse.get_pos()
            if (self.antivirus_button.checkForInput(mousePos)):
                self.grabbing = True
                self.grabbed = antivirus()

            if (self.firewall_button.checkForInput(mousePos)):
                self.grabbing = True
                self.grabbed = firewall()

            if (self.twoFA_button.checkForInput(mousePos)):
                self.grabbing = True
                self.grabbed = twoFactorAuth()

        elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.grabbing == True) and self.balance >= self.grabbed.cost:
            # Verify if the drop is in an allowed block and drop the tower
            self.allTowers.append([self.grabbed.__class__(), pygame.mouse.get_pos()])
            self.balance -= self.grabbed.cost

@dataclass
class HelpOptions(GameLoop):
    """
    Handle with help options menu
    """
    back_button: Button

    @classmethod
    def create(cls, screen, state):
        help_options = cls(
            screen = screen,
            state = state,
            back_button = Button(image=None, pos=(480, 600), 
                            text_input="Back", font=get_font(25), base_color="White",
                            hovering_color="Green")
        )
        return help_options


    def loop(self, game):
        self.state = game.state
        clock = pygame.time.Clock()
        self.screen.fill("black")
        help_text = get_font(25).render("This is the Help screen.", True, "White")
        help_rect = help_text.get_rect(center=(480, 260))
        self.screen.blit(help_text, help_rect)

        while self.state == GameState.help_options:
            mouse_pos = pygame.mouse.get_pos()

            self.handle_events(game)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)

            self.back_button.changeColor(mouse_pos)
            self.back_button.update(self.screen)


    def handle_event(self, event, game):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.checkForInput(mouse_pos):
                game.set_state(GameState.main_menu)
                self.state = GameState.main_menu
