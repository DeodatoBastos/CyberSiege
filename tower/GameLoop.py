from tower.constants import *
from tower.states import GameState
from tower.enemies.sql_injection import Sql_Injection
from tower.button import Button
from tower.resources import get_font
from tower.towers import antivirus, firewall, twoFactorAuth, Towers
from tower.map import map1
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
    board : map1

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
            grabbed = False,
            board = map1()
        )
        return game_playing
    
    def validatePlacing(self,mouse_pos):
        #map mouse position to corresponding square, returns True/False + the correct (x,y) position to place the tower
        col_index = mouse_pos[0]//32
        line_index = mouse_pos[1]//32
        if self.board.placeable[line_index][col_index] == 0:
            return False, None
        
        else:
            self.board.placeable[line_index][col_index] = 0
            offset = 0
            return True, (32*col_index + 16 + offset, 32*line_index + 16 + offset)
    
    def renderThings(self):
        # Rendering the buttons
        for btn in self.allButtons:
            btn.update(self.screen)

        # Render deployed towers along with a square to show they are placed
        for element in self.allTowers:
            square = pygame.Surface((32,32))
            square = square.convert_alpha()
            square.fill((100,255,100,128))
            self.screen.blit(square,(element[1][0]-16,element[1][1]-16,32,32))
            self.screen.blit(pygame.transform.scale(element[0].img, (32,32)), (element[1][0] - 16, element[1][1] - 16))

        # while grabbing something, render it at mouse position each frame
        if (self.grabbing):
            self.screen.blit(pygame.transform.scale(self.grabbed.img, (32,32)), (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))

    def loop(self, game):
        self.state = game.state
        clock = pygame.time.Clock()
        sql = Sql_Injection()
        self.allButtons = [self.antivirus_button, self.firewall_button, self.twoFA_button]

        while self.state == GameState.game_playing:
            self.handle_events(game)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            self.screen.blit(IMAGE_SPRITES[(False, False, "map01")], (0, 0))
            sql.draw(game.screen)
            sql.draw_health_bar(game.screen)
            sql.move()
            clock.tick(DESIRED_FPS)
            self.renderThings()
                
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
            check, placePos = self.validatePlacing(pygame.mouse.get_pos())
            if (check):
                self.allTowers.append([self.grabbed.__class__(), placePos])
                self.balance -= self.grabbed.cost
            
            

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
