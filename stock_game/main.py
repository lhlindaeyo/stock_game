import pygame
from core import GameCore, draw_top
from chart import draw_chart

# 초기화
pygame.init()
FONT = pygame.font.Font("BMDOHYEON_ttf.ttf", 24)

screen = pygame.display.set_mode((800,650))
pygame.display.set_caption("재벌집 막내 손주")
clock = pygame.time.Clock()

game = GameCore(FONT)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            game.keyboard(event)

    game.update()

    screen.fill((0, 0, 0))
    draw_top(screen, game, FONT) # 게임 상단 그리기
    game.draw(screen) # 게임 요소 그리기

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

