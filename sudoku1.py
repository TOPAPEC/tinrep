import random

class SudokuGame:

    @staticmethod
    def start_new_game():
        print("Enter number of filled cells on the game field:")
        filled_cells_number = SudokuGame.__get_new_game_input()
        return GameState(filled_cells_number)

    @staticmethod
    def load_game():
        print("Enter name of save file:")
        file_name = input()
        while len(file_name) < 5 or file_name[-4:-1] != '.plk':
            print('You should enter .plk save file. Try again:')
            file_name = input()
        try:
            field = SudokuGame.__parse_game_save_file(file_name)
        except Exception as e:
            print('Failed to load game:' + str(e))

    @staticmethod
    def __get_new_game_input():
        filled_cells_string = input()
        while filled_cells_string.isdigit():
            print('Wrong input. Enter an integer from [0;81]')
            filled_cells_string = input()
        return int(filled_cells_string)

    @staticmethod
    def __parse_game_save_file(filename):
        return 1

    # Class that contains all method for field initialisation.
    class FieldCreator:

        @staticmethod
        def create_field(filled_cells_number):
            field = [[] for j in range(9)]

        @staticmethod
        def add_random_numbers(filled_cells_number, field):
            base_line = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for i in range(3):
                for j in range(3):
                    field[i*3+j] = SudokuGame.FieldCreator.cyclic_shift_of_array(base_line, i + j * 3)
            count_zero_inserted = 0
            for i in range(9):
                for j in range(9):
                    if count_zero_inserted >= 81 - filled_cells_number:
                        break
                    field[i][j] = 0
                    count_zero_inserted += 1
                if count_zero_inserted >= 81 - filled_cells_number:
                    break
            return field
        @staticmethod
        def cyclic_shift_of_array(array, number):
            return array[number:] + array[0:number]

class GameState:

    def __init__(self, field):
        self.__field = field

    @staticmethod
    def load_game(field):
        loaded_game = GameState()
        loaded_game.__field = field
        return loaded_game

    # Saves the game into a file.
    def save_game(self):
        return

    # Let player make another move.
    def make_move(self):
        return

    # Gets and parses move's command.
    def __parse_move_input(self):
        return

    # Changes cell's state.
    def __change_cell_state(self, row, column, num):
        return


field = SudokuGame.FieldCreator.add_random_numbers(10, [[] for j in range(9)])
for i in range(len(field)):
    print(field[i])
