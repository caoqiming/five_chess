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
    # It is currently the opponent's (white) turn,
    # and the next_move is where the opponent must move.
    next_move: List[Tuple[int, int]]


class chess:
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int32)
    round_n = 0
    history = []
    game_over = False

    def validate(self, x: int, y: int) -> bool:
        return x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE

    def get_board(self):
        return self.board.copy()

    def set_board(self, board):
        self.board = board.copy()
        self.history.clear()
        self.round_n = 0
        self.game_over = False

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
    # 用于辅助输入的参数
    current_index = 0

    def __init__(self, name):
        self.name = name

    def get_situation_from_board(self, board: np.ndarray) -> situation:
        s = situation()
        # get size of this situation and the localtion in the board.
        i_min, i_max, j_min, j_max = BOARD_SIZE - 1, 0, BOARD_SIZE - 1, 0
        for i in range(0, BOARD_SIZE):
            for j in range(0, BOARD_SIZE):
                if board[i][j] != EMPTY:
                    if i < i_min:
                        i_min = i
                    if i > i_max:
                        i_max = i
                    if j < j_min:
                        j_min = j
                    if j > j_max:
                        j_max = j
        size_x, size_y = i_max - i_min + 1, j_max - j_min + 1
        s.board = np.zeros((size_x, size_y), dtype=np.int32)
        # convert board to situation's board
        for i in range(0, size_x):
            for j in range(0, size_y):
                color = board[i + i_min][j + j_min]
                if color == WHITE or color == BLACK or color == GREEN:
                    s.board[i][j] = color
                elif color == RED:
                    s.next_move.append((i, j))

    def get_board_from_situation(self, s: situation) -> np.ndarray:
        board = board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int32)
        x, y = s.board.shape
        # 将situation显示到中央
        x_shift, y_shift = int((BOARD_SIZE - x) / 2), int((BOARD_SIZE - y) / 2)
        for i in range(0, x):
            for j in range(0, y):
                board[i + x_shift][j + y_shift] = s.board[i][j]
        for one in s.next_move:
            board[one[0] + x_shift][one[1] + y_shift] = RED
        return board

    def append_situation_from_board(self, board: np.ndarray):
        situation = self.get_situation_from_board(board)
        self.data.append(situation)

    def dump(self):
        with open("./data/%s.dat" % (self.name), "wb") as file:
            pickle.dump(self.data, file)

    def load(self):
        with open("./data/%s.dat" % (self.name), "rb") as file:
            self.data = pickle.load(file)

    # 查看当前记录
    def get_current_situation_board(self):
        s = self.data[self.current_index]
        return self.get_board_from_situation(s)

    def print(self):
        print(
            "situations: %s \ntotal: %d current: %d\n"
            % (self.name, len(self.data), self.current_index + 1)
        )

    def over_write_current_situation(self, board: np.ndarray):
        situation = self.get_situation_from_board(board)
        self.data[self.current_index] = situation

    def delete_current_situation(self):
        del self.data[self.current_index]

    def set_current_index(self, value: int):
        self.current_index == value
        if self.current_index < 0 or self.current_index >= len(self.data):
            print("invalid index: %d\n" % (self.current_index))
            self.current_index = 0
        self.print()

    # 识别situation
    def fit(self, board: np.ndarray, s: situation, x_shift: int, y_shift: int) -> bool:
        for one in s.next_move:
            if board[one[0] + x_shift][one[1] + y_shift] != EMPTY:
                return False
        x, y = s.board.shape
        for i in range(0, x):
            for j in range(0, y):
                want_color = s.board[i][j]
                if want_color == EMPTY:
                    continue
                color = board[i + x_shift][j + y_shift]
                if want_color == GREEN and color != EMPTY:
                    return False
                if (want_color == WHITE or want_color == BLACK) and color != want_color:
                    return False
        return True

    def check_situation(
        self, board: np.ndarray, s: situation
    ) -> List[List[Tuple[int, int]]]:
        ans = []
        x, y = s.board.shape
        x_shift_max, y_shift_max = BOARD_SIZE - x, BOARD_SIZE - y
        for i in range(0, x_shift_max):
            for j in range(0, y_shift_max):
                if self.fit(board, s, i, j):
                    temp = []
                    for one in s.next_move:
                        temp.append((one[0] + i, one[1] + j))
                    ans.append(temp)
        return ans

    # return true if win
    def check_situations(self, board: np.ndarray) -> bool:
        next_move = set()
        inited = False
        for s in self.data:
            next_move_list = self.check_situation(board, s)
            for one in next_move_list:  # one is a fited situation
                temp_move = set()
                for one_point in one:
                    temp_move.add(one_point)
                if not inited:
                    next_move = temp_move
                    inited = True
                else:
                    next_move = next_move & temp_move
                    if len(next_move) == 0:
                        return True

        return False


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
