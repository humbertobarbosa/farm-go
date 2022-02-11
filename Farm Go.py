import pygame
from pygame.locals import *
from sys import exit
from scripts import Soil
from scripts import Waterfont
from scripts import Player
from scripts import Store
from scripts import Trash
from scripts import Fence


pygame.init()
#region Constants
WIDTH = int(pygame.display.Info().current_w/2)
HEIGHT = int(pygame.display.Info().current_h/2)
TITLE = "Farm Go"
FPS = 60
BACKGROUND_IMAGE = pygame.image.load("data/sprites/scenary/background.png")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
SCALE = WIDTH/256
PLAYER_WIDTH = int(SCALE * 16)
#endregion

class FarmGo:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
    
    def newGame(self):
        #* all sprites that will be rendered
        self.allSprites = YsortGroup()
        #* Dedicated to colision
        self.collideSprites = pygame.sprite.Group()
        #* Dedicated to soil (cause it isn't affected by layer order)
        self.soilsSprite = pygame.sprite.Group()

        #* Draw Level
        self.soils = self.drawGrid(int(SCALE * 16), int(WIDTH/7), int(HEIGHT/2.5))
        self.waterfont = Waterfont.Waterfont((int((WIDTH/8)*4.4), int(HEIGHT/4)), int(SCALE * 64), [self.allSprites, self.collideSprites])
        #self.store = Store.Store((int(WIDTH/2.185), 0), int(SCALE * 128), [self.allSprites, self.collideSprites])
        
        self.trash = Trash.Trash((int(WIDTH/2), int(2*SCALE)), int(SCALE * 32), [self.allSprites, self.collideSprites])
        
        self.fence_right = Fence.Fence((int(WIDTH - 33*SCALE), int(44*SCALE)), [self.collideSprites, self.allSprites], (int(SCALE*8), int(91*SCALE)), "side")
        self.fence_left = Fence.Fence((int(15*SCALE), int(44*SCALE)), [self.collideSprites, self.allSprites], (int(SCALE*8), int(91*SCALE)), "side_2")
        self.fence_bottom = Fence.Fence((int(15*SCALE), int((HEIGHT - 21.5*SCALE))), [self.collideSprites, self.allSprites], (int(SCALE*128), int(22*SCALE)), "bottom")

        #* Draw Player
        self.player = Player.Player(int((WIDTH/2) - (PLAYER_WIDTH/2)), int((HEIGHT/2) - (PLAYER_WIDTH*1.5/2)), PLAYER_WIDTH, PLAYER_WIDTH/10, self.collideSprites)

        self.allSprites.add(self.player)
        self.soilsSprite.add(self.soils)

        #self.soilsSprite.add(self.player)
        self.run()
    
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.updateSprites()
            self.drawSprites()

    def checkSoilColision(self):
        for sprite in self.soils:
            if sprite.hitbox.colliderect(self.player.rect):
                if self.player.selectedSoil != {}:
                    if self.player.selectedSoil != sprite:
                        self.player.selectedSoil.Deselect()
                        self.player.selectedSoil = sprite
                        self.player.selectedSoil.Select()
                else:
                    self.player.selectedSoil = sprite
                    self.player.selectedSoil.Select()          
            else:
                if self.player.selectedSoil != {}:
                    self.player.selectedSoil.Deselect()
                    self.player.selectedSoil = {}

    def events(self):
        self.checkSoilColision()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.running:
                    self.running = False
                    pygame.quit()
                    exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.screen = pygame.display.set_mode((int(WIDTH/2), int(HEIGHT/2)))

                if event.key == K_w:
                    self.player.vertical = -1
                elif event.key == K_s:
                    self.player.vertical = 1
                if event.key == K_a:
                    self.player.horizontal = -1
                elif event.key == K_d:
                    self.player.horizontal = 1
            if event.type == KEYUP:
                if event.key == K_w or event.key == K_s:
                    self.player.vertical = 0
                if event.key == K_a or event.key == K_d:
                    self.player.horizontal = 0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.player.selectedSoil != {}:
                        self.player.selectedSoil.Interact()
    
    def updateSprites(self):
        self.allSprites.update()
        self.soilsSprite.update()
        

    def drawSprites(self):
        self.screen.blit(BACKGROUND_IMAGE, (0, 0))
        self.soilsSprite.draw(self.screen)
        #self.allSprites.draw(self.screen)
        self.allSprites.Custom_draw()
        for sprite in self.soilsSprite:
            pygame.draw.rect(self.screen, (255, 255, 255), sprite.hitbox)

        pygame.draw.rect(self.screen, (255, 0, 0), self.player.hitbox)
        pygame.display.flip()

    def drawGrid(self, cellsize, width, height):
        soils = list()
        gap = int(cellsize/16)
        for i in range(4):
            for j in range(3):
                solo = Soil.Soil((width + i * cellsize + gap*i, height + j * cellsize + gap*j), cellsize)
                soils.append(solo)
        return soils


class YsortGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.display_surface = pygame.display.get_surface()

    def Custom_draw(self):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            self.display_surface.blit(sprite.image, sprite.rect)

game = FarmGo()
game.newGame()


