import pygame
import sys
from pygame.locals import *
import chess

BOARD_SIZE = 600
MARGIN_SIZE = 30
BLOCK_SIZE = BOARD_SIZE / chess.BOARD_SIZE
PIECE_SIZE = BLOCK_SIZE * 0.45
# pygame 初始化
pygame.init()

# 设置背景颜色和线条颜色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# 设置背景框大小
size = width, height = BOARD_SIZE + 2 * MARGIN_SIZE, BOARD_SIZE + 2 * MARGIN_SIZE
# 设置帧率，返回clock 类
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("chess")

five_chess = chess.chess()


def convert_pos_to_index(x):
    x -= MARGIN_SIZE
    x = round(x / BLOCK_SIZE)
    if x < 0:
        x = 0
    if x >= chess.BOARD_SIZE:
        x = chess.BOARD_SIZE - 1
    return x


def handle_click(x, y):
    x = convert_pos_to_index(x)
    y = convert_pos_to_index(y)
    five_chess.game_put(x, y)
    result = five_chess.check_position(x, y)
    if result == chess.BLACK:
        print("BLACK WIN!")
    elif result == chess.WHITE:
        print("WHITE WIN!")
    return


def handle_key(key):
    if key == pygame.K_r:
        five_chess.reset()
    elif key == pygame.K_BACKSPACE:
        five_chess.regrate()
    return


while True:
    for event in pygame.event.get():
        # 查找关闭窗口事件
        if event.type == QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos[0], event.pos[1])
        elif event.type == pygame.KEYDOWN:
            handle_key(event.key)

    # 填充背景色
    screen.fill(WHITE)

    # draw board
    pygame.draw.lines(
        screen,
        BLACK,
        closed=1,
        points=[
            (MARGIN_SIZE, MARGIN_SIZE),
            (MARGIN_SIZE + BOARD_SIZE, MARGIN_SIZE),
            (MARGIN_SIZE + BOARD_SIZE, MARGIN_SIZE + BOARD_SIZE),
            (MARGIN_SIZE, MARGIN_SIZE + BOARD_SIZE),
        ],
        width=2,
    )

    # 绘制棋盘
    for i in range(0, chess.BOARD_SIZE):
        pygame.draw.line(
            screen,
            BLACK,
            (MARGIN_SIZE, MARGIN_SIZE + round(i * BLOCK_SIZE)),
            (MARGIN_SIZE + BOARD_SIZE, MARGIN_SIZE + round(i * BLOCK_SIZE)),
            1,
        )
        pygame.draw.line(
            screen,
            BLACK,
            (MARGIN_SIZE + round(i * BLOCK_SIZE), MARGIN_SIZE),
            (MARGIN_SIZE + round(i * BLOCK_SIZE), MARGIN_SIZE + BOARD_SIZE),
            1,
        )

    # 绘制棋子
    for i in range(0, chess.BOARD_SIZE):
        for j in range(0, chess.BOARD_SIZE):
            if five_chess.board[i][j] == chess.EMPTY:
                continue
            if five_chess.board[i][j] == chess.BLACK:
                pygame.draw.circle(
                    screen,
                    BLACK,
                    (
                        MARGIN_SIZE + round(i * BLOCK_SIZE),
                        MARGIN_SIZE + round(j * BLOCK_SIZE),
                    ),
                    radius=PIECE_SIZE,
                )
            else:
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (
                        MARGIN_SIZE + round(i * BLOCK_SIZE),
                        MARGIN_SIZE + round(j * BLOCK_SIZE),
                    ),
                    radius=PIECE_SIZE,
                )
                pygame.draw.circle(
                    screen,
                    BLACK,
                    (
                        MARGIN_SIZE + round(i * BLOCK_SIZE),
                        MARGIN_SIZE + round(j * BLOCK_SIZE),
                    ),
                    radius=PIECE_SIZE,
                    width=1,
                )

    # 刷新
    pygame.display.flip()

    clock.tick(60)
