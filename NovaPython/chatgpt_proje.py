import pygame
import sys

# Ekran boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)

    def update(self):
        pass

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Geometry Dash Clone")
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit
