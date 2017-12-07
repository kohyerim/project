import pygame
import random
from Image import Image
from Fish import Fish

pygame.display.init()
pygame.init()
pygame.font.init()

FONT = pygame.font.Font('resources/CALIBRATE1.ttf', 50)


class Screen:
    width = 1000
    height = 600
    pygame.display.set_mode((width, height))
    penguin_img = Image('resources/penguin.png')
    penguin_frame = [penguin_img.get_image(48 * 9, 48, 48, 48),
                     penguin_img.get_image(48 * 10, 48, 48, 48),
                     penguin_img.get_image(48 * 11, 48, 48, 48)]
    penguin_move_frame = [penguin_img.get_image(48 * 9, 48 * 5, 48, 48),
                          penguin_img.get_image(48 * 10, 48 * 5, 48, 48),
                          penguin_img.get_image(48 * 11, 48 * 5, 48, 48)]
    fish_img = Image('resources/fish_sprite.png')
    fish_frame = [fish_img.get_image(0, 48 * 2, 48, 48),
                  fish_img.get_image(48, 48 * 2, 48, 48),
                  fish_img.get_image(48 * 2, 48 * 2, 48, 48)]
    fish_now = fish_frame[0]
    background = pygame.image.load('resources/background.jpg')
    menu_background = pygame.image.load('resources/menu_background.jpg')
    over_background = pygame.image.load('resources/game-over background_Resized.png')
    food_background = pygame.image.load('resources/food_back-resized.jpg')
    enemy_background = pygame.image.load('resources/enemy-resized.jpg')
    back_button = pygame.image.load('resources/button-back-Resized.png')

    def __init__(self):
        pygame.display.set_caption("Game")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.blit(self.menu_background, (0, 0))
        self.penguin_x = 800
        self.penguin_y = 300
        self.wait = True
        self.last_update = 0
        self.current_frame = 0
        self.image = self.penguin_frame[0]
        self.score = 0
        self.heart = 3
        self.num = 0

    def text(self, text, font, color, x, y):  # 텍스트 그리는 함수
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        rect.midtop = (x, y)
        self.screen.blit(surface, rect)

    def penguin_animate(self, state, move):
        now = pygame.time.get_ticks()
        if not move:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.penguin_frame)
                if state:
                    self.image = pygame.transform.flip(self.penguin_frame[self.current_frame], True, False)
                else:
                    self.image = self.penguin_frame[self.current_frame]
        elif move:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.penguin_frame)
                self.image = self.penguin_move_frame[self.current_frame]

    def food_animate(self, frame):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.fish_frame)
        return frame[self.current_frame]

    def menu(self):
        start = False
        start_button = pygame.image.load('resources/button-start-game3.png')

        while not start:
            start_rect = self.screen.blit(start_button, (350, 400))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        start = True

    def start(self):
        finish = False
        food_button = pygame.image.load('resources/food70.png')
        penguin_move = False
        penguin_state = True
        self.penguin_x = 800
        self.penguin_y = 300

        while not finish:
            self.penguin_animate(penguin_state, penguin_move)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.image, (self.penguin_x, self.penguin_y))
            food_button_rect = self.screen.blit(food_button, (900, 500))
            if penguin_move and self.penguin_x > 320:
                self.penguin_x -= 3
                if self.penguin_x < 500:
                    self.penguin_y += 1.5
            elif self.penguin_x <= 350:
                finish = True
            elif not penguin_move:
                if penguin_state:
                    self.penguin_x += 1
                    if self.penguin_x >= 800:
                        penguin_state = False
                elif not penguin_state:
                    self.penguin_x -= 1
                    if self.penguin_x <= 600:
                        penguin_state = True
            if self.heart <= 0:
                finish = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if food_button_rect.collidepoint(event.pos):
                        penguin_move = True
                        self.num = random.randint(0, 10)
                        print("랜덤값 : %d " % self.num)
            pygame.display.update()

    def food(self):
        finish = False
        penguin_x = 200
        penguin_y = 200
        fish_list = []
        fish_rect_list = []
        count = random.randint(10, 15)
        for i in range(0, count):
            fish = Fish(self.screen, self.food_animate(self.fish_frame), random.randint(0, 300), random.randint(50, 500), self.fish_frame)
            fish_list.append(fish)
            fish_rect_list.append(fish)

        while not finish:
            penguin = pygame.transform.flip(self.penguin_move_frame[0], True, False)
            self.screen.blit(self.food_background, (0, 0))
            penguin_rect = self.screen.blit(penguin, (penguin_x, penguin_y))
            back_button_rect = self.screen.blit(self.back_button, (20, 20))
            self.text("FOOD", FONT, (0, 0, 0), self.width/2, self.height/4)

            for fish in fish_list:
                rect = fish.move()
                fish_rect_list.pop(0)
                fish_rect_list.append(rect)

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                if -20 < penguin_y:
                    penguin_y -= 3
            if pressed[pygame.K_DOWN]:
                if penguin_y < 600 - 48:
                    penguin_y += 3
            if pressed[pygame.K_RIGHT]:
                if penguin_x < 1000 - 48:
                    penguin_x += 3
            if pressed[pygame.K_LEFT]:
                if -10 < penguin_x:
                    penguin_x -= 3

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        finish = True

            for fish in fish_rect_list:
                if penguin_rect.colliderect(fish):
                    self.score += 5
                    print(self.score)

            pygame.display.update()

    def enemy(self):
        finish = False
        test = pygame.Surface((50, 50))
        test.fill((255, 255, 0))
        self.heart -= 1
        print("남은 생명 : %d" % self.heart)
        while not finish:
            pygame.display.update()
            self.screen.blit(self.enemy_background, (0, 0))
            self.text("ENEMY", FONT, (0, 0, 0), self.width / 2, self.height / 4)
            test_rect = self.screen.blit(test, (100, 500))
            if self.heart <= 0:
                finish = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if test_rect.collidepoint(event.pos):
                        finish = True

    def choice(self, num):
        if num >= 7:
            self.enemy()
        else:
            self.food()

    def game_over(self):
        self.score = 0
        self.heart = 3
        over = False
        replay_button = pygame.Surface((50, 50))
        replay_button.fill((15, 80, 98))
        gameover_button = pygame.Surface((50, 50))
        gameover_button.fill((30, 25, 55))
        while not over:
            self.screen.blit(self.over_background, (0, 0))
            self.text("GAME OVER", FONT, (0, 0, 0), self.width / 2, self.height / 4)
            replay_button_rect = self.screen.blit(replay_button, (400, 400))
            gameover_button_rect = self.screen.blit(gameover_button, (300, 400))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_button_rect.collidepoint(event.pos):
                        over = True
                    elif gameover_button_rect.collidepoint(event.pos):
                        exit(0)


game = Screen()
game.menu()
play = True
while True:
    play = True
    while play:
        game.start()
        game.choice(game.num)
        if game.heart == 0:
            play = False
    game.game_over()

