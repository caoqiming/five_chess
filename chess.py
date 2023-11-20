import numpy as np
import pickle
from typing import List, Dict, Tuple

BOARD_SIZE = 15
EMPTY = 0
BLACK = 1
WHITE = 2
RED = 3  # for record mode, force move
GREEN = 4  # for record mode, empty
DIRECNTIONS = [
    ((-1, 0), (1, 0)),
    ((0, -1), (0, 1)),
    ((-1, -1), (1, 1)),
    ((-1, 1), (1, -1)),
]


class situation:
    board: np.ndarray
    next_move: List[Tuple[int, int]]  # next is black turn


class chess:
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int32)
    round_n = 0
    history = []
    game_over = False

    def validate(self, x: int, y: int) -> bool:
        return x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE

    def get_board(self):
        return self.board

    def reset(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE))
        self.history.clear()
        self.round_n = 0
        self.game_over = False

    def regrate(self):
        if self.round_n > 0:
            self.round_n -= 1
            pos = self.history.pop()
            self.board[pos[0], pos[1]] = EMPTY
            self.game_over = False

    def show(self):
        print(self.board)

    def put(self, x: int, y: int, color: int, force: bool = False):
        if not force and (self.game_over or self.board[x][y] != EMPTY):
            return

        if color != BLACK and color != WHITE and color != RED and color != GREEN:
            raise Exception("fail to put, invalid color %d" % (color))
        self.board[x][y] = color

    def game_put(self, x: int, y: int):
        if self.board[x][y] != EMPTY:
            return

        self.round_n += 1
        if self.round_n % 2 == 1:
            self.put(x, y, BLACK)
        else:
            self.put(x, y, WHITE)
        self.history.append((x, y))

    def check_position(self, x: int, y: int) -> int:
        current_color = self.board[x][y]
        if current_color == EMPTY:
            return EMPTY

        for direcntion in DIRECNTIONS:
            counter = 1
            for current_direction in direcntion:
                temp_x, temp_y = x, y
                while self.validate(temp_x, temp_y):
                    temp_x += current_direction[0]
                    temp_y += current_direction[1]
                    if self.board[temp_x][temp_y] == current_color:
                        counter += 1
                        if counter >= 5:  # game over
                            self.game_over = True
                            return current_color
                    else:
                        break
        return EMPTY

    def check_position_and_get_adjacent_with_mask(self, x: int, y: int, mask: int):
        adjacent = [(x, y, 15)]
        current_color = self.board[x][y]
        if current_color == EMPTY:
            return EMPTY, adjacent

        for index, direcntion in enumerate(DIRECNTIONS):
            if mask & 1 << index:
                continue

            counter = 1
            for current_direction in direcntion:
                temp_x, temp_y = x, y
                while self.validate(temp_x, temp_y):
                    temp_x += current_direction[0]
                    temp_y += current_direction[1]
                    if self.board[temp_x][temp_y] == current_color:
                        counter += 1
                        adjacent.append((temp_x, temp_y, 1 << index))  # 标记该位置i方向已检查过了
                        if counter >= 5:
                            return current_color, adjacent
                    else:
                        break
        return EMPTY, adjacent

    def check_all(self) -> int:
        mask = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int32)
        for i in range(0, BOARD_SIZE):
            for j in range(0, BOARD_SIZE):
                if self.board[i][j] == EMPTY:
                    continue

                winner, adjacent = self.check_position_and_get_adjacent_with_mask(
                    i, j, mask[i][j]
                )
                if winner != EMPTY:
                    return winner

                for one in adjacent:
                    mask[one[0]][one[1]] |= one[2]
        return EMPTY

    def save_record(self) -> situation:
        s = situation()
        s.board = self.board.copy()
        return


class situations:
    name: str = "unnamed"
    data: List[situation] = []

    def __init__(self, name):
        self.name = name

    def append(self, s: situation):
        self.data.append(s)

    def dump(self):
        with open("./data/%s.dat" % (self.name), "wb") as file:
            pickle.dump(self.data, file)

    def load(self):
        with open("./data/%s.dat" % (self.name), "rb") as file:
            self.data = pickle.load(file)


class chess_palyer:
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int32)

    def set_board(self, new_board: np.ndarray):
        self.board = new_board

    def move(self):
        return

    def sub_matrix_exists(matrix, sub_matrix):
        rows, cols = matrix.shape
        sub_rows, sub_cols = sub_matrix.shape
        for i in range(rows - sub_rows + 1):
            for j in range(cols - sub_cols + 1):
                if np.array_equal(
                    matrix[i : i + sub_rows, j : j + sub_cols], sub_matrix
                ):
                    return True
        return False

    def force_move(self):
        return


if __name__ == "__main__":
    ss = situations("test")
    s = situation()
    s.board = np.zeros((3, 3), dtype=np.int32)
    s.next_move = [(2, 3)]
    ss.append(s)
    s = situation()
    s.board = np.zeros((3, 3), dtype=np.int32)
    s.next_move = [(2, 2)]
    ss.append(s)
    print(ss.data[0].next_move)
    print(ss.data[1].next_move)
