import pygame
import time

pygame.init()

HEIGHT, WIDTH = 450, 450
SIZE_CASE = 150
FPS = 30
TEMPS_MAX = 15

screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("TIC TAC TOE")

timer = pygame.time.Clock()
running = True 

class Game():
    def __init__(self):
        self.position = [0]*9
        self.tour = 1 
        self.list_grille = self.grille() 
        self.placement = []
        self.win = False
        self.temps_ecoule = False
        self.font = pygame.font.SysFont(None, 55)
        self.font_symboles = pygame.font.SysFont(None, 120)
        self.font_timer = pygame.font.SysFont(None, 30)
        self.button_restart = pygame.Rect(0, HEIGHT // 2 - 45, WIDTH, 90)
        self.start_time = time.time()
        self.elapsed_time = 0
        for j in range(3):
            for i in range(3):
                self.placement.append((i*SIZE_CASE, j*SIZE_CASE))
    
    def grille(self):
        list = []
        for j in range(3):
            for i in range(3):
                case = pygame.Rect(i*SIZE_CASE, j*SIZE_CASE, SIZE_CASE, SIZE_CASE)
                list.append(case)
        return list
    
    def affichage(self):
        for case in self.list_grille:
            pygame.draw.rect(screen,pygame.Color("#ffffff"), case, width=1)
        
        for index, nb in enumerate(self.position):
            if nb == 1:
                text_x = self.font_symboles.render('X', True, pygame.Color("#BA1200"))
                screen.blit(text_x, (self.placement[index][0] + 45, self.placement[index][1] + 25))
            
            if nb == 2:
                text_o = self.font_symboles.render('O', True, pygame.Color("#9DD1F1"))
                screen.blit(text_o, (self.placement[index][0] + 45, self.placement[index][1] + 25))
        
        
        if self.win or self.temps_ecoule: 
            pygame.draw.rect(screen, pygame.Color("#C8E0F4"), self.button_restart)
            
            if self.temps_ecoule:
                text = self.font.render("Temps écoulé! :(", True, pygame.Color("#508AA8"))
            elif 0 not in self.position:
                text = self.font.render("Match nul! :|", True, pygame.Color("#508AA8"))
            else:
                text = self.font.render("Joueur {} a gagné! :)".format(2 if self.tour == 1 else 1), True, pygame.Color("#508AA8"))
            
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    
    def click(self, pos):
        if (self.win or self.temps_ecoule):
            if self.button_restart.collidepoint(pos):
                self.restart()
                return
        
        for i in self.list_grille:
            if i.collidepoint(pos):
                self.action_jeu(self.list_grille.index(i))
        
    def action_jeu(self, index):
        if not self.win and not self.temps_ecoule:
            if self.position[index] == 0:
                self.position[index] = self.tour 
                if self.tour == 1:
                    self.tour = 2
                else:
                    self.tour = 1

        # Vérifications de victoire 
        if self.position[0] == self.position[1] == self.position[2] != 0:
            self.win = True
        elif self.position[3] == self.position[4] == self.position[5] != 0:
            self.win = True
        elif self.position[6] == self.position[7] == self.position[8] != 0:
            self.win = True
        elif self.position[0] == self.position[4] == self.position[8] != 0:
            self.win = True
        elif self.position[2] == self.position[4] == self.position[6] != 0:
            self.win = True
        elif self.position[0] == self.position[3] == self.position[6] != 0:
            self.win = True
        elif self.position[1] == self.position[4] == self.position[7] != 0:
            self.win = True
        elif self.position[2] == self.position[5] == self.position[8] != 0:
            self.win = True
        
    def restart(self):
        self.position = [0]*9
        self.tour = 1
        self.win = False
        self.temps_ecoule = False
        self.start_time = time.time()
        self.elapsed_time = 0

    def update_timer(self):
        if not self.win and not self.temps_ecoule:
            self.elapsed_time = int(time.time() - self.start_time)
            
            
            if self.elapsed_time >= TEMPS_MAX:
                self.temps_ecoule = True

    def display_timer(self):
        
        temps_restant = max(0, TEMPS_MAX - self.elapsed_time)
        timer_text = self.font_timer.render(f"Temps: {temps_restant} s", True, pygame.Color("#ffffff"))
        screen.blit(timer_text, (10, 10))

game = Game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            game.click(pos)
    
    game.update_timer()
    
    screen.fill(pygame.Color("#031927"))
    game.affichage()
    game.display_timer()

    pygame.display.update()
    timer.tick(FPS)
