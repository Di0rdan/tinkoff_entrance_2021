import sudoku
import pickle


class Game:
    def __init__(self):
        pass

    def start(self):
        mode = '#'
        while mode != '1' and mode != '2':
            print('Введите 1 для запуска режима игры для пользователя')
            print('Введите 2 для запуска режима игры для компьюетера')
            mode = input().strip()
        if mode == '1':
            game.startUserGame()
        elif mode == '2':
            game.startComputerGame()

    def startUserGame(self):
        command = None
        while command != 'new' and command != 'upload':
            print('Для начала новой игры введите new, для загрузки предыдущей введите upload')
            command = input()
        if command == 'new':
            self.__play(self.__get_new_grid())
        elif command == 'upload':
            try:
                self.__play(self.__upload())
            except FileNotFoundError:
                print('файл data.pkl с сохраненной игрой не был найден, поэтому была запущена новая игра')
                self.__play(self.__get_new_grid())
            except ValueError:
                print('файл с игрой содержит невалидные данные, поэтому была запущена новая игра')
                self.__play(self.__get_new_grid())
            except pickle.UnpicklingError:
                print('файл с игрой содержит невалидные данные, поэтому была запущена новая игра')
                self.__play(self.__get_new_grid())
            except:
                print('что-то пошло не так, поэтому была запущена новая игра')
                self.__play(self.__get_new_grid())

    def startComputerGame(self):
        grid = sudoku.Grid(0)
        filled = self.__ask_integer_number(0, 81)
        while grid.get_filled_count() < filled:
            print(grid)
            print('Введите три целых числа в одной строке:\n'
                  'номера строки и столбца клетки(нумерация с нуля), а также значение, '
                  'которое следует поставить в данную клетку')
            try:
                grid.modify(*map(int, input().split()))
            except sudoku.GridError as ge:
                print(ge)
            except:
                print('что-то пошло не так :(')
        print('Спасибо, достаточное количество клеток заполнено')
        try:
            for step in grid.solve():
                print(*step)
            print(grid)
        except sudoku.GridError as ge:
            print(ge)

    def __play(self, grid):
        while not grid.is_filled():
            print(grid)
            print('Введите три целых числа в одной строке:\n'
                  'номера строки и столбца клетки(нумерация с нуля), а также значение, '
                  'которое следует поставить в данную клетку\n'
                  'Для выхода из игры введите exit')
            command = input().strip()
            if command == 'exit':
                self.__save(grid)
                break
            try:
                grid.modify(*map(int, command.split()))
            except sudoku.GridError as ge:
                print(ge)
            except:
                print('что-то пошло не так :(')
        else:
            print('Молодец! Задача успешно решена!\n')

    def __ask_integer_number(self, min_val=0, max_val=81):
        user_value = None
        while not isinstance(user_value, int) or \
                user_value < min_val or \
                user_value > max_val:
            print('Введите количество заполненных клеток от 0 до 81')
            try:
                user_value = int(input())
            except ValueError:
                print('введите целое значние')
        return user_value

    def __get_new_grid(self):
        return sudoku.Grid(self.__ask_integer_number(0, 81), 3)

    def __save(self, grid):
        with open('data.pkl', 'wb') as f:
            pickle.dump(grid, f)

    def __upload(self):
        with open('data.pkl', 'rb') as f:
            grid = pickle.load(f)
        if not isinstance(grid, sudoku.Grid):
            raise ValueError
        return grid


if __name__ == '__main__':
    game = Game()
    game.start()
