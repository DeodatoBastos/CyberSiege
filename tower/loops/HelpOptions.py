import pygame
from .GameLoop import GameLoop
from tower.constants import *
from tower.states import GameState
from tower.button import Button
from tower.resources import get_font
from dataclasses import dataclass
import os

@dataclass
class HelpOptions(GameLoop):
    """
    Handle with help options menu
    """
    back_menu_button: Button
    back_page_button: Button
    forward_page_button: Button
    page_counter: int
    num_pages = 8
    arrowright_img : pygame.Surface
    mouseleft_img : pygame.Surface
    mouseright_img : pygame.Surface
    av_img : pygame.Surface
    firewall_img : pygame.Surface
    twoFa_img : pygame.Surface
    vpn_img : pygame.Surface
    coin_img : pygame.Surface
    tutorial01_img : pygame.Surface
    green_button_img : pygame.Surface
    red_button_img : pygame.Surface
    play_img : pygame.Surface
    pause_img : pygame.Surface
    heart_img : pygame.Surface
    tutorialFim_img : pygame.Surface

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
            page_counter = 1,

            arrowright_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "ARROWRIGHT.png")),
            (64, 64)),
            mouseleft_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "MOUSEBUTTONLEFT.png")),
            (64, 64)),
            mouseright_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "MOUSEBUTTONRIGHT.png")),
            (64, 64)),

            av_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "antivirus.png")),
            (64, 64)),
            firewall_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "firewall.png")),
            (64, 64)),
            twoFa_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "2FA.png")),
            (64, 64)),
            vpn_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "vpn.png")),
            (64, 64)),

            coin_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "GoldCoin.png")),
            (64, 64)),
            tutorial01_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "tutorial01.jpg")),
            (240, 140)),
            green_button_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "green_button.png")),
            (64, 64)),
            red_button_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "red_button.png")),
            (64, 64)),
            play_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "Play.png")),
            (64, 64)),
            pause_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "Pause.png")),
            (64, 64)),
            heart_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "heart.png")),
            (100, 140)),
            tutorialFim_img = pygame.transform.scale(
            pygame.image.load(os.path.join("tower", "assets", "sprites", "tutorialFim.jpg")),
            (600, 360)),
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

            if self.page_counter == 1:
                self.draw_first_page()
            elif self.page_counter == 2:
                self.draw_second_page()
            elif self.page_counter == 3:
                self.draw_third_page()
            elif self.page_counter == 4:
                self.draw_fourth_page()
            elif self.page_counter == 5:
                self.draw_fifth_page()
            elif self.page_counter == 6:
                self.draw_sixth_page()
            elif self.page_counter == 7:
                self.draw_seventh_page()
            elif self.page_counter == 8:
                self.draw_eight_page()


    def handle_event(self, event, game):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_menu_button.checkForInput(mouse_pos):
                self.page_counter = 1
                game.set_state(GameState.main_menu)
                self.state = GameState.main_menu
            if self.back_page_button.checkForInput(mouse_pos):
                if (self.page_counter > 1):
                    self.page_counter -= 1
            if self.forward_page_button.checkForInput(mouse_pos):
                if (self.page_counter < self.num_pages):
                    self.page_counter += 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.page_counter = 1
                game.set_state(GameState.main_menu)
                self.state = GameState.main_menu
            if event.key == pygame.K_LEFT:
                if (self.page_counter > 1):
                    self.page_counter -= 1
            if event.key == pygame.K_RIGHT:
                if (self.page_counter < self.num_pages):
                    self.page_counter += 1

    def draw_first_page(self):
        self.screen.fill("black")
        text_input = f"Bem vindo ao tutorial de\n" + \
                     f"Cyber Siege! Pressione      ou\n" + \
                     f"clique nas setas para avançar"
        
        lines = text_input.split("\n")
        texts = [get_font(25).render(line, True, "white") for line in lines]
        for i, text in enumerate(texts):
            self.screen.blit(text, (100,220 + 64*i))
        self.screen.blit(self.arrowright_img,(690,265))

        number_page = get_font(30).render(f" 1/{self.num_pages} ", True, "White")
        number_page_rect = number_page.get_rect(center=(480, 600))
        self.screen.blit(number_page, number_page_rect)
        self.update_buttons()


    def draw_second_page(self):
        self.screen.fill("black")
        text_input = f"O objetivo deste jogo é se defender\n" + \
                     f"de ataques cibernéticos. Para isso,\n" + \
                     f"você deve utilizar torres de defesa."
        
        lines = text_input.split("\n")
        texts = [get_font(25).render(line, True, "white") for line in lines]
        for i, text in enumerate(texts):
            self.screen.blit(text, (50,150 + 64*i))

        self.screen.blit(self.av_img,(200,400))
        self.screen.blit(self.firewall_img,(350,400))
        self.screen.blit(self.twoFa_img,(500,400))
        self.screen.blit(self.vpn_img,(650,400))
        number_page = get_font(30).render(f" 2/{self.num_pages} ", True, "White")
        number_page_rect = number_page.get_rect(center=(480, 600))
        self.screen.blit(number_page, number_page_rect)
        self.update_buttons()

    def draw_third_page(self):
        self.screen.fill("black")
        text_input = f"Para comprar uma torre, basta a\n" + \
                     f"selecionar com     e em seguida\n" + \
                     f"clicar em um slot válido. Você\n" + \
                     f"perderá dinheiro no processo.\n" + \
                     f"Para soltar uma torre selecionada,\n" + \
                     f"pressione     ."
                     
        
        lines = text_input.split("\n")
        texts = [get_font(25).render(line, True, "white") for line in lines]
        for i, text in enumerate(texts):
            self.screen.blit(text, (100,100 + 64*i))

        self.screen.blit(self.mouseleft_img,(480,140))
        self.screen.blit(self.mouseright_img,(360,400))
        number_page = get_font(30).render(f" 3/{self.num_pages} ", True, "White")
        number_page_rect = number_page.get_rect(center=(480, 600))
        self.screen.blit(number_page, number_page_rect)
        self.update_buttons()
    
    def draw_fourth_page(self):
        self.screen.fill("black")
        text_input = f"O seu dinheiro aparecerá no canto\n" + \
                     f"inferior esquerdo da tela. Não se\n" + \
                     f"preocupe em gastá-lo. Você pode\n" + \
                     f"ganhar mais dinheiro dos inimigos."
                     
        
        lines = text_input.split("\n")
        texts = [get_font(25).render(line, True, "white") for line in lines]
        for i, text in enumerate(texts):
            self.screen.blit(text, (100,100 + 64*i))

        money= get_font(40).render("100", True, "White")
        self.screen.blit(money, (100,500))
        self.screen.blit(self.coin_img,(220,490))

        number_page = get_font(30).render(f" 4/{self.num_pages} ", True, "White")
        number_page_rect = number_page.get_rect(center=(480, 600))
        self.screen.blit(number_page, number_page_rect)
        self.update_buttons()

    def draw_fifth_page(self):
        self.screen.fill("black")
        text_input = f"Torres podem ser melhoradas ou\n" + \
                     f"vendidas. Para realizar essas ações,\n" + \
                     f"clique em uma torre já colocada, e\n" + \
                     f"um menu com informações se abrirá.\n" + \
                     f"     -> upgrade\n" + \
                     f"     -> vende a torre\n"
        
        lines = text_input.split("\n")
        texts = [get_font(25).render(line, True, "white") for line in lines]
        for i, text in enumerate(texts):
            self.screen.blit(text, (50,100 + 64*i))
        self.screen.blit(self.tutorial01_img, (620, 350))
        self.screen.blit(self.green_button_img, (100, 336))
        self.screen.blit(self.red_button_img, (100, 400))
        number_page = get_font(30).render(f" 5/{self.num_pages} ", True, "White")
        number_page_rect = number_page.get_rect(center=(480, 600))
        self.screen.blit(number_page, number_page_rect)
        self.update_buttons()

    def draw_sixth_page(self):
        self.screen.fill("black")
        text_input = f"Os ataques são divididos em hordas.\n" + \
                    f"Você saberá que uma horda chegou ao\n" + \
                    f"final quando o botão    mudar para\n" + \
                    f"   , no canto inferior direito da\n" + \
                    f"tela. Aproveite esse momento para\n" + \
                    f"descansar e melhorar suas torres.\n" + \
                    f"Para continuar, pressione o \n"
                    
        
        lines = text_input.split("\n")
        texts = [get_font(25).render(line, True, "white") for line in lines]
        for i, text in enumerate(texts):
            self.screen.blit(text, (50,100 + 64*i))
        self.screen.blit(self.pause_img,(565,210))
        self.screen.blit(self.play_img,(50,270))
        self.screen.blit(self.play_img,(750,467))
        number_page = get_font(30).render(f" 6/{self.num_pages} ", True, "White")
        number_page_rect = number_page.get_rect(center=(480, 600))
        self.screen.blit(number_page, number_page_rect)
        self.update_buttons()
    
    def draw_seventh_page(self):
        self.screen.fill("black")
        text_input = f"Cuidado ao deixar o inimigo se\n" + \
                     f"aproximar à vontade, o seu núcleo\n" + \
                     f"não é invencível! Quando a contagem\n" + \
                     f"de corações chegar a 0, você perde.\n" + \
                     f"Mantenha-os longe!\n"
                     
        
        lines = text_input.split("\n")
        texts = [get_font(25).render(line, True, "white") for line in lines]
        for i, text in enumerate(texts):
            self.screen.blit(text, (50,100 + 64*i))
        self.screen.blit(get_font(40).render("10",True,"White"), (400,470))
        self.screen.blit(self.heart_img, (480,410))

        number_page = get_font(30).render(f" 7/{self.num_pages} ", True, "White")
        number_page_rect = number_page.get_rect(center=(480, 600))
        self.screen.blit(number_page, number_page_rect)
        self.update_buttons()    
   
    def draw_eight_page(self):
        self.screen.fill("black")
        
        text = get_font(40).render("Divirta-se!", True, "white")

        self.screen.blit(text, (270,465))
        self.screen.blit(self.tutorialFim_img, (180,50))

        number_page = get_font(30).render(f" 8/{self.num_pages} ", True, "White")
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
