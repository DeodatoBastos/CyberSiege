import os
import time
import random
import pygame
from .GameLoop import GameLoop
from tower.constants import *
from tower.states import GameState
from tower.button import Button
from tower.resources import get_font
from dataclasses import dataclass
from tower.map import map1
from tower.enemies import Sql_Injection, DDOS
from tower.towers import antivirus, firewall, twoFactorAuth, Towers

play_img =  pygame.transform.scale(pygame.image.load(os.path.join("tower", "assets", "sprites", "play.png")),(32, 32))
pause_img =  pygame.transform.scale(pygame.image.load(os.path.join("tower", "assets", "sprites", "pause.png")),(32, 32))

@dataclass
class GamePlaying(GameLoop):

    antivirus_button : Button
    firewall_button: Button
    twoFA_button : Button
    action_button: Button
    allButtons : "list[Button]"
    allTowers : "list[Towers,(int,int)]"
    is_paused : bool
    is_playing: bool
    balance : int
    grabbing : bool
    grabbed : bool
    board : map1
    number_enemies : list
    round : int
    enemies : list
    timer : int

    @classmethod
    def create(cls, screen, state):
        game_playing = cls(
            screen = screen,
            state = state,
            antivirus_button = Button(image=antivirus.img,pos=(896+33,64),text_input="",font=get_font(1),base_color="#d7fcd4", hovering_color="ffffff"),
            firewall_button = Button(image=firewall.img,pos=(896+33,160),text_input="",font=get_font(1),base_color="#d7fcd4", hovering_color="ffffff"),
            twoFA_button = Button(image=twoFactorAuth.img,pos=(896+33,258),text_input="",font=get_font(1),base_color="#d7fcd4", hovering_color="ffffff"),
            action_button = Button(image=play_img, pos=(896+32,580),text_input="",font=get_font(1),base_color="#d7fcd4", hovering_color="ffffff"),
            allButtons = [],
            is_paused = True,
            is_playing = False,
            allTowers = [],
            balance = 100,
            grabbing = False,
            grabbed = False,
            board = map1(),
            number_enemies = [[10, 5], [20, 10], [30, 20]], # Each row is a round. Each column is the quantity of enemies
                                                # Right now, the sequence of enemies is SQL, ddos
            round = 0,
            enemies = [],
            timer = 0
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
        # render play and pause
        if self.is_paused:
            self.action_button = Button(image=play_img, pos=(896+32, 580),text_input="",font=get_font(1),base_color="#d7fcd4", hovering_color="ffffff")
        else:
            self.action_button = Button(image=pause_img, pos=(896+32, 580),text_input="",font=get_font(1),base_color="#d7fcd4", hovering_color="ffffff")

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
        
        # Generates waves
        if sum(self.current_wave) == 0:
            if len(self.enemies) == 0:
                self.round += 1
                self.current_wave = self.number_enemies[self.round]
                self.is_paused = True
                self.is_playing = False
        elif self.is_playing:
            wave_enemies = [Sql_Injection(), DDOS()]
            for x in range(len(self.current_wave)):
                if time.time() - self.timer >= random.randrange(1,6)/3:
                    self.timer = time.time()
                    if self.current_wave[x] != 0:
                        self.enemies.append(wave_enemies[x])
                        self.current_wave[x] = self.current_wave[x] - 1
                        break

        if not self.is_paused:
            for enemy in self.enemies:
                enemy.draw(self.screen)

            to_del = []
            for en in self.enemies:
                en.move()
                if en.path_pos >= len(en.path) - 1:
                    to_del.append(en)

            # delete all enemies off the screen
            for d in to_del:
                # Remove comment when lives are implemented
                #self.lives -= 1
                self.enemies.remove(d)

    def loop(self, game):
        pygame.mixer.music.load(os.path.join("tower", "assets", "audio", "music.mp3"))
        pygame.mixer.music.play(loops=-1)
        self.state = game.state
        clock = pygame.time.Clock()
        self.current_wave = self.number_enemies[self.round][:]

        while self.state == GameState.game_playing:
            self.allButtons = [self.antivirus_button, self.firewall_button, self.twoFA_button, 
                               self.action_button]
            self.handle_events(game)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            self.screen.blit(IMAGE_SPRITES[(False, False, "map01")], (0, 0))
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

            if self.action_button.checkForInput(mousePos) and not self.is_playing:
                self.is_paused = not self.is_paused
                self.is_playing = True

        elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.grabbing == True) and self.balance >= self.grabbed.cost:
            # Verify if the drop is in an allowed block and drop the tower
            check, placePos = self.validatePlacing(pygame.mouse.get_pos())
            if (check):
                self.allTowers.append([self.grabbed.__class__(), placePos])
                self.balance -= self.grabbed.cost