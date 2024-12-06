import pygame
from pygame.locals import *
import sys
import random

class DoodleJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.green = pygame.image.load("green.png").convert_alpha()
        self.blue = pygame.image.load("blue.png").convert_alpha()
        self.red = pygame.image.load("red.png").convert_alpha()
        self.red_1 = pygame.image.load("red_1.png").convert_alpha()
        self.playerRight = pygame.image.load("right.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("right_1.png").convert_alpha()
        self.playerLeft = pygame.image.load("left.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("left_1.png").convert_alpha()
        self.spring = pygame.image.load("spring.png").convert_alpha()
        self.spring_1 = pygame.image.load("spring_1.png").convert_alpha()
        self.font = pygame.font.SysFont("Arial", 25)

        self.score = 0
        self.level = 1  # Start at level 1
        self.level_up_score = 1000  # Score threshold to increase level
        self.playerx = 400
        self.playery = 400
        self.platforms = [[400, 500, 0, 0]]
        self.springs = []
        self.cameray = 0
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0
        self.direction = 0

    def level_up(self):
        if self.score >= self.level_up_score:
            self.level += 1
            self.level_up_score += 1000  # Increase threshold for next level
            print(f"Level Up! You are now on Level {self.level}.")

    def updatePlayer(self):
        if not self.jump:
            self.playery += self.gravity
            self.gravity += 1
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1

        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.xmovement < 10:
                self.xmovement += 1
            self.direction = 0
        elif key[K_LEFT]:
            if self.xmovement > -10:
                self.xmovement -= 1
            self.direction = 1
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1

        if self.playerx > 850:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 850
        self.playerx += self.xmovement

        if self.playery - self.cameray <= 200:
            self.cameray -= 10

        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))

    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.green.get_width() - 10, self.green.get_height())
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 10, self.playerRight.get_height())
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                if p[2] != 2:
                    self.jump = 15
                    self.gravity = 0
                else:
                    p[-1] = 1

            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5 + self.level  # Increase platform speed based on level
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5 + self.level  # Increase platform speed based on level
                    if p[0] <= 0:
                        p[-1] = 1

    def drawPlatforms(self):
        for p in self.platforms:
            check = self.platforms[1][1] - self.cameray
            if check > 600:
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2

                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                coords = self.platforms[-1]
                check = random.randint(0, 1000)
                if check > 900 and platform == 0:
                    self.springs.append([coords[0], coords[1] - 25, 0])
                self.platforms.pop(0)
                self.score += 100

            if p[2] == 0:
                self.screen.blit(self.green, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.blue, (p[0], p[1] - self.cameray))
            elif p[2] == 2:
                if not p[3]:
                    self.screen.blit(self.red, (p[0], p[1] - self.cameray))
                else:
                    self.screen.blit(self.red_1, (p[0], p[1] - self.cameray))

        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cameray))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))

            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(pygame.Rect(self.playerx, self.playery, self.playerRight.get_width(), self.playerRight.get_height())):
                self.jump = 50
                self.cameray -= 50

    def generatePlatforms(self):
        on = 600
        while on > -100:
            x = random.randint(0, 700)
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = 0
            elif platform < 900:
                platform = 1
            else:
                platform = 2
            self.platforms.append([x, on, platform, 0])
            on -= 50

    def drawGrid(self):
        for x in range(80):
            pygame.draw.line(self.screen, (222,222,222), (x * 12, 0), (x * 12, 600))
            pygame.draw.line(self.screen, (222,222,222), (0, x * 12), (800, x * 12))

    def game_over(self):
        game_over_font = pygame.font.SysFont("Arial", 50)
        game_over_text = game_over_font.render(f"Game Over! Final Score: {self.score}", True, (255, 0, 0))
        self.screen.blit(game_over_text, (200, 250))
        restart_text = self.font.render("Press 'R' to Restart or 'Q' to Quit", True, (0, 0, 0))
        self.screen.blit(restart_text, (250, 300))
        pygame.display.flip()

    def reset_game(self):
        self.score = 0
        self.level = 1
        self.platforms = [[400, 500, 0, 0]]
        self.springs = []
        self.playerx = 400
        self.playery = 400
        self.cameray = 0

    def run(self):
        clock = pygame.time.Clock()
        self.generatePlatforms()

        while True:
            self.screen.fill((255, 255, 255))
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:  # Restart game
                        self.reset_game()
                    elif event.key == K_q:  # Quit game
                        sys.exit()

            if self.playery - self.cameray > 700:
                self.game_over()

            self.level_up()  # Check for level up
            self.drawGrid()
            self.updatePlayer()
            self.updatePlatforms()
            self.drawPlatforms()

            score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
            level_text = self.font.render(f"Level: {self.level}", True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(level_text, (10, 40))

            pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    game = DoodleJump()
    game.run()

