import pygame
import random
import sys

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("블럭깨기 게임")
clock = pygame.time.Clock()

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 패들 클래스
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 15))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.speed = 7

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# 공 클래스
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed_x = 5
        self.speed_y = -5

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 벽에 튕김
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y
        
        # 게임오버
        if self.rect.top >= SCREEN_HEIGHT:
            return False
        return True

# 블럭 클래스
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((75, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))

# 스프라이트 그룹
paddle_group = pygame.sprite.Group(Paddle())
ball_group = pygame.sprite.Group(Ball())
block_group = pygame.sprite.Group()

# 블럭 생성
for row in range(4):
    for col in range(10):
        block_group.add(Block(col * 80, row * 25 + 30))

score = 0
font = pygame.font.Font(None, 36)
game_over = False

# 게임 루프
running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        paddle_group.update()
        ball_group.update()
        
        ball = ball_group.sprites()[0]
        paddle = paddle_group.sprites()[0]

        # 공이 패들과 충돌
        if pygame.sprite.spritecollide(ball, paddle_group, False):
            ball.speed_y = -ball.speed_y

        # 공이 블럭과 충돌
        hit_blocks = pygame.sprite.spritecollide(ball, block_group, True)
        if hit_blocks:
            ball.speed_y = -ball.speed_y
            score += len(hit_blocks) * 10

        # 공이 화면 밖으로 나감
        if ball.rect.top >= SCREEN_HEIGHT:
            game_over = True

        # 모든 블럭 파괴됨
        if len(block_group) == 0:
            game_over = True

    # 화면 그리기
    screen.fill(BLACK)
    paddle_group.draw(screen)
    ball_group.draw(screen)
    block_group.draw(screen)

    # 점수 표시
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        if len(block_group) == 0:
            end_text = font.render("You Win!", True, GREEN)
        else:
            end_text = font.render("Game Over!", True, RED)
        screen.blit(end_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()