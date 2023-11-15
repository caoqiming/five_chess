import numpy as np

BOARD_SIZE = 15
EMPTY = 0
BLACK = 1
WHITE = 2
DIRECNTIONS = [
    ((-1, 0), (1, 0)),
    ((0, -1), (0, 1)),
    ((-1, -1), (1, 1)),
    ((-1, 1), (1, -1)),
]


class chess:
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int32)
    round_n = 0
    history = []
    game_over = False

    def validate(self, x: int, y: int) -> bool:
        return x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE

    def set_board(self, newboard):
        self.board = newboard

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

    def put(self, x: int, y: int, color: int):
        if self.game_over:
            return

        if color != BLACK and color != WHITE:
            raise Exception("fail to put, invalid color %d" % (color))
        if self.board[x][y] != EMPTY:
            raise Exception("fail to put, (%d,%d) is not empty" % (x, y))
        self.board[x][y] = color

    def game_put(self, x: int, y: int):
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


class chess_palyer:
    def move(self):
        return


if __name__ == "__main__":
    a = chess()
    a.put(1, 1, 2)
    a.put(1, 2, 2)
    a.put(1, 3, 2)
    a.put(1, 4, 2)
    a.put(2, 1, 2)
    a.put(2, 2, 2)
    a.put(2, 3, 2)
    a.put(2, 4, 2)
    print(a.check_all())
    a.put(1, 5, 2)

    print(a.check_all())

    a.show()
