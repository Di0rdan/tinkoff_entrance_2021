from random import randrange, random


class GridError(Exception):
    def __init__(self, text, *args):
        self.txt = text


class Grid:
    def __init__(self, filled=30, n=3):
        if not isinstance(filled, int) or \
                not isinstance(n, int):
            raise (TypeError('arguments must be integer'))
        self.subtable_size = n
        self.filled_count = filled
        self.table_size = n * n
        self.table = [[((i * n + i // n + j) % (n * n) + 1)
                       for j in range(self.table_size)] for i in range(self.table_size)]
        self.__shuffle()
        self.mutable = [[False] * self.table_size for _ in range(self.table_size)]
        random_poses_list = sorted(
            [(i, j) for i in range(self.table_size)
             for j in range(self.table_size)],
            key=lambda x: random()
        )[:self.table_size ** 2 - filled]
        for pos in random_poses_list:
            self.mutable[pos[0]][pos[1]] = True
            self.table[pos[0]][pos[1]] = '*'

    def __str__(self):
        grid_str = ' '.join([' ', '|'] + list(map(str, range(0, self.table_size)))) + \
                   '\n' + '--' * (self.table_size + 2) + '\n'
        for i in range(self.table_size):
            grid_str += str(i) + ' | ' + ' '.join(map(str, self.table[i])) + '\n'
        return grid_str


    def modify(self, posX, posY, val):
        if not isinstance(posX, int) or \
                not isinstance(posY, int) or \
                not (isinstance(val, int)):
            raise TypeError('arguments must be integer')
        if posX < 0 or posX >= self.table_size:
            raise GridError('row number must be between 0 and ' + str(self.table_size - 1))
        if posY < 0 or posY >= self.table_size:
            raise GridError('column number must be between 0 and ' + str(self.table_size - 1))
        if val < 1 or val > self.table_size:
            raise GridError('cell\'s value must be between 1 and ' + str(self.table_size))
        if not self.mutable[posX][posY]:
            raise GridError('that is unmutable cell')
        if val in self.table[posX]:
            raise GridError('the row already contains this value')
        if val in [self.table[i][posY] for i in range(self.table_size)]:
            raise GridError('the column already contains this value')
        if val in [self.table[i][j]
                   for i in range(posX // self.subtable_size * self.subtable_size,
                                  (posX // self.subtable_size + 1) * self.subtable_size)
                   for j in range(posY // self.subtable_size * self.subtable_size,
                                 (posY // self.subtable_size + 1) * self.subtable_size)]:
            raise GridError('the subsquare already contains this value')
        self.__modify(posX, posY, val)

    def __modify(self, posX, posY, val):
        if self.table[posX][posY] == '*' and val != '*':
            self.filled_count += 1
        if self.table[posX][posY] != '*' and val == '*':
            self.filled_count -= 1
        self.table[posX][posY] = val

    def solve(self):
        solve_list = []
        self.__solve(solve_list)
        if not self.is_filled():
            raise GridError('no solutions found')
        else:
            return solve_list

    def __solve(self, lst):
        if self.is_filled():
            return
        pos = 0
        while self.table[pos // self.table_size][pos % self.table_size] != '*':
            pos += 1
        posX, posY = pos // self.table_size, pos % self.table_size
        for val in range(1, 1 + self.table_size):
            if val not in self.table[posX] and \
                val not in [self.table[i][posY] for i in range(self.table_size)] and \
                val not in [self.table[i][j]
                           for i in range(posX // self.subtable_size * self.subtable_size,
                                          (posX // self.subtable_size + 1) * self.subtable_size)
                           for j in range(posY // self.subtable_size * self.subtable_size,
                                         (posY // self.subtable_size + 1) * self.subtable_size)]:
                self.__modify(posX, posY, val)
                lst.append((posX, posY, val))
                self.__solve(lst)
                if self.is_filled():
                    return
                self.__modify(posX, posY, '*')
                lst.pop()

    def __swap_rows(self, subrow, row1, row2):
        row1 = subrow * self.subtable_size + row1
        row2 = subrow * self.subtable_size + row2
        self.table[row1], self.table[row2] = \
            self.table[row2], self.table[row1]

    def __swap_columns(self, subcolumn, column1, column2):
        column1 = subcolumn * self.subtable_size + column1
        column2 = subcolumn * self.subtable_size + column2
        for row in range(self.subtable_size ** 2):
            self.table[row][column1], self.table[row][column2] = \
                self.table[row][column2], self.table[row][column1]

    def __swap_subrows(self, subrow1, subrow2):
        for i in range(self.subtable_size):
            self.table[subrow1 * self.subtable_size + i], \
            self.table[subrow2 * self.subtable_size + i] = \
                self.table[subrow2 * self.subtable_size + i], \
                self.table[subrow1 * self.subtable_size + i]

    def __swap_subcolumns(self, subcolumn1, subcolumn2):
        for i in range(self.subtable_size):
            for row in range(self.subtable_size ** 2):
                self.table[row][subcolumn1 * self.subtable_size + i], \
                self.table[row][subcolumn2 * self.subtable_size + i] = \
                    self.table[row][subcolumn2 * self.subtable_size + i], \
                    self.table[row][subcolumn1 * self.subtable_size + i]

    def __shuffle(self, depth=81):
        for _ in range(depth):
            self.__swap_rows(randrange(0, self.subtable_size, 1),
                             *sorted(
                                 range(0, self.subtable_size),
                                 key=lambda x: random())[:2]
                             )
            self.__swap_columns(randrange(0, self.subtable_size, 1),
                                *sorted(
                                    range(0, self.subtable_size),
                                    key=lambda x: random())[:2]
                                )
            self.__swap_subrows(*sorted(range(0, self.subtable_size),
                                        key=lambda x: random())[:2])
            self.__swap_subcolumns(*sorted(range(0, self.subtable_size),
                                           key=lambda x: random())[:2])

    def get_filled_count(self):
        return self.filled_count

    def is_filled(self):
        return self.filled_count == self.table_size ** 2
