import pygame
import random
from Image import Image
from Fish import Fish

pygame.display.init()
pygame.init()
pygame.font.init()

FONT = pygame.font.Font('resources/CALIBRATE1.ttf', 25)


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
    whale_img = Image('resources/whale_sprite.png')
    whale_frame = [whale_img.get_image(0, 0, 100, 100),
                   whale_img.get_image(100, 0, 100, 100),
                   whale_img.get_image(200, 0, 100, 100)]
    whale_now = whale_frame[0]
    background = pygame.image.load('resources/background.jpg')
    menu_background = pygame.image.load('resources/menu_background.jpg')
    over_background = pygame.image.load('resources/game-over background_Resized.png')
    food_background = pygame.image.load('resources/food_back-resized.jpg')
    enemy_background = pygame.image.load('resources/enemy-resized.jpg')
    back_button = pygame.image.load('resources/button-back-Resized.png')
    start_button = pygame.image.load('resources/button-start-game3.png')
    replay_button = pygame.image.load('resources/button-play-again-resized.png')
    life = Image('resources/heart_Resized2.png')  # 라이프 이미지 불러오기
    life_list = [life.get_image(0, 0, 36, 44),  # 꽉 찬 하트
                 life.get_image(36, 0, 36, 44)]  # 빈 하트

    def __init__(self):
        pygame.display.set_caption("Game")
        self.screen = pygame.display.set_mode((self.width, self.height))
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

    def animate(self, frame):
        now = pygame.time.get_ticks()
        if now - self.last_update > 150:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.fish_frame)
        return frame[self.current_frame]

    def menu(self):
        start = False

        while not start:
            self.screen.blit(self.menu_background, (0, 0))
            start_rect = self.screen.blit(self.start_button, (350, 400))
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
            self.text("SCORE  :  ", FONT, (0, 0, 0), 60, 10)
            self.text(str(self.score), FONT, (0, 0, 0), 130, 10)
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
            if self.heart == 3:
                self.screen.blit(self.life_list[0], (10 + 850, 10))
                self.screen.blit(self.life_list[0], (50 + 850, 10))
                self.screen.blit(self.life_list[0], (90 + 850, 10))
            elif self.heart == 2:
                self.screen.blit(self.life_list[0], (10 + 850, 10))
                self.screen.blit(self.life_list[0], (50 + 850, 10))
                self.screen.blit(self.life_list[1], (90 + 850, 10))
            elif self.heart == 1:
                self.screen.blit(self.life_list[0], (10 + 850, 10))
                self.screen.blit(self.life_list[1], (50 + 850, 10))
                self.screen.blit(self.life_list[1], (90 + 850, 10))
            pygame.display.update()

    def food(self):
        finish = False
        penguin = pygame.transform.flip(self.penguin_move_frame[0], True, False)
        penguin_x = 10
        penguin_y = self.height/2
        fish_rect_list = []
        count = random.randint(10, 20)
        for i in range(0, count):
            fish = Fish(self.screen, self.animate(self.fish_frame), random.randint(70, 300), random.randint(50, 500), self.fish_frame)
            fish_rect_list.append(fish)

        while not finish:
            self.screen.blit(self.food_background, (0, 0))
            penguin_rect = self.screen.blit(penguin, (penguin_x, penguin_y))
            back_button_rect = self.screen.blit(self.back_button, (850 + 20, 20))
            self.text("FOOD", FONT, (0, 0, 0), self.width/2, self.height/4)
            self.text("SCORE  :  ", FONT, (0, 0, 0), 60, 10)
            self.text(str(self.score), FONT, (0, 0, 0), 130, 10)

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
                    penguin = pygame.transform.flip(self.penguin_move_frame[0], True, False)
            if pressed[pygame.K_LEFT]:
                if -10 < penguin_x:
                    penguin_x -= 3
                    penguin = self.penguin_move_frame[0]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        finish = True

            for fish in fish_rect_list:
                if penguin_rect.colliderect(fish):
                    self.score += 5
                    fish_rect_list.remove(fish)
                fish.move()
            pygame.display.update()

    def enemy(self):
        finish = False
        penguin = pygame.transform.flip(self.penguin_move_frame[0], True, False)
        penguin_x = 280
        penguin_y = self.height/2
        whale_x = 10
        penguin_rect = self.screen.blit(penguin, (280, self.height / 2))
        back_button_rect = None
        while not finish:
            pygame.display.update()
            self.screen.blit(self.enemy_background, (0, 0))
            whale = self.animate(self.whale_frame)
            whale_rect = self.screen.blit(whale, (whale_x, penguin_y - 30))
            whale_x += 2.05
            penguin_x += 1.55
            self.text("ENEMY", FONT, (0, 0, 0), self.width / 2, self.height / 4)
            if self.heart <= 0:
                finish = True
            if not whale_rect.colliderect(penguin_rect):
                penguin_rect = self.screen.blit(penguin, (penguin_x, penguin_y))
            if whale_x >= 990:
                back_button_rect = self.screen.blit(self.back_button, (850 + 20, 20))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        finish = True

    def choice(self, num):
        if num >= 8:
            self.enemy()
            self.heart -= 1
        else:
            self.food()

    def game_over(self):
        self.score = 0
        self.heart = 3
        over = False
        while not over:
            self.screen.blit(self.over_background, (0, 0))
            self.text("GAME OVER", FONT, (0, 0, 0), self.width / 2, self.height / 4)
            replay_button_rect = self.screen.blit(self.replay_button, (850 + 20, 20))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_button_rect.collidepoint(event.pos):
                        over = True


game = Screen()

play = True
while True:
    play = True
    game.menu()
    while play:
        game.start()
        game.choice(game.num)
        if game.heart == 0:
            play = False
    game.game_over()

