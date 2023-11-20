import pygame
import sys
from pygame.locals import *
import chess

BOARD_SIZE = 600
MARGIN_SIZE = 30
BLOCK_SIZE = BOARD_SIZE / chess.BOARD_SIZE
PIECE_SIZE = BLOCK_SIZE * 0.45

PVP = 0
PVE = 1
RECORD = 2
MODE = PVP

# record 模式相关变量
record_current_color = chess.BLACK
record_situations = chess.situations("new_record")
record_situation = chess.situation()
# 用于展示的棋盘
five_chess = chess.chess()

# pygame ui相关
pygame.init()
WHITE = (255, 255, 255)
GREEN = (42, 222, 108)
RED = (250, 17, 45)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
size = width, height = BOARD_SIZE + 2 * MARGIN_SIZE, BOARD_SIZE + 2 * MARGIN_SIZE
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("chess")


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
    if MODE == PVP:
        five_chess.game_put(x, y)
        result = five_chess.check_position(x, y)
        if result == chess.BLACK:
            print("BLACK WIN!")
        elif result == chess.WHITE:
            print("WHITE WIN!")
    elif MODE == RECORD:
        five_chess.put(x, y, record_current_color, force=True)
    return


def handle_key(key):
    global record_current_color
    global record_situations
    global record_situation
    if key == pygame.K_r:
        five_chess.reset()
    elif key == pygame.K_BACKSPACE:
        five_chess.regrate()
    if MODE == RECORD:
        if key == pygame.K_w:
            record_current_color = chess.WHITE
        elif key == pygame.K_b:
            record_current_color = chess.BLACK
        elif key == pygame.K_f:  # force next move
            record_current_color = chess.RED
        elif key == pygame.K_g:  # need to be empty
            record_current_color = chess.GREEN
        elif key == pygame.K_n:  # next situation
            record_situations.append(record_situation)
            record_situation = chess.situation()
            five_chess.reset()
        elif key == pygame.K_s:  # save
            record_situations.dump()
    return


def spin():
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
                position = (
                    MARGIN_SIZE + round(i * BLOCK_SIZE),
                    MARGIN_SIZE + round(j * BLOCK_SIZE),
                )
                if five_chess.board[i][j] == chess.BLACK:
                    pygame.draw.circle(screen, BLACK, position, radius=PIECE_SIZE)
                elif five_chess.board[i][j] == chess.WHITE:
                    pygame.draw.circle(screen, WHITE, position, radius=PIECE_SIZE)
                    pygame.draw.circle(
                        screen, BLACK, position, radius=PIECE_SIZE, width=1
                    )
                elif five_chess.board[i][j] == chess.RED:
                    pygame.draw.circle(screen, RED, position, radius=PIECE_SIZE)
                elif five_chess.board[i][j] == chess.GREEN:
                    pygame.draw.circle(screen, GREEN, position, radius=PIECE_SIZE)

        # 刷新
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "record":
            MODE = RECORD

    spin()
