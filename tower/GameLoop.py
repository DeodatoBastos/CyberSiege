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
from tower.towers import antivirus,firewall,twoFactorAuth
class MainGame(GameLoop):
    def loop(self, game):
        self.state = game.state
        clock = pygame.time.Clock()

        #Defining Tower templates for the buttons to refeer cause i dunno a better way to do it
        av_template = antivirus()
        firewall_template = firewall()
        twoFA_template = twoFactorAuth()

        #Defining the buttons (tower selection)
        antivirus_button = button(av_template, 896 + 5, 32, 64,64, 54,'')
        firewall_button = button(firewall_template, 896 + 5, 128, 64,64, 54,'')
        twoFA_button = button(twoFA_template, 896 + 5, 224, 64,64, 54,'')
        allButtons = [antivirus_button, firewall_button, twoFA_button]

        #Grabbing tower state
        grabbing = False
        grabbed = None
        allTowers = []

        #money
        balance = 100

        while self.state == GameState.game_playing:
            #self.handle_events(game)                      implementing my own
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)
            self.screen.blit(IMAGE_SPRITES[(False, False, "background")], (0, 0))

            #Rendering the buttons
            for b in allButtons:
                b.draw(self.screen)

            #Render deployed towers
            for element in allTowers:
                self.screen.blit(pygame.transform.scale(IMAGE_SPRITES[(False, False, element[0].imageStr)], (32,32)), (element[1][0] - 16, element[1][1] - 16))

            #while grabbing something, render it at mouse position each frame
            if (grabbing):
                self.screen.blit(pygame.transform.scale(IMAGE_SPRITES[(False, False, grabbed.imageStr)], (32,32)), (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))

            #Search for inputs (eu fiz isso aqui pq precisava acessar o allButtons)
            for event in pygame.event.get():
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3):
                    grabbing = False
                    grabbed = None

                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and grabbing == False):
                    #Checar se clicou em algum button
                    for b in allButtons:
                        if b.isOver(pygame.mouse.get_pos()):
                            #Grab the correct sprite
                            grabbing = True
                            grabbed = b.tower


                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and grabbing == True) and balance >= grabbed.cost:
                    #Ver se soltou em uma área válida, e dar deploy na torre naquele lugar caso sim
                    allTowers.append([grabbed, pygame.mouse.get_pos()])
                    balance -= grabbed.cost
                    

                if (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ) or event.type == pygame.QUIT:
                    game.set_state(GameState.quitting)
                    self.state = GameState.quitting

