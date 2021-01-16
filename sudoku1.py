import random
import os
import hashlib


class SudokuGame:

    @staticmethod
    def start_new_game():
        print("Enter number of filled cells on the game field:")
        filled_cells_number = SudokuGame.__get_new_game_input()
        return GameState(SudokuGame.FieldCreator.create_field(filled_cells_number))

    @staticmethod
    def load_game():
        print("Enter name of save file:")
        file_name = input()
        field = []
        print(file_name[-4:])
        while len(file_name) < 5 or file_name[-4:] != '.plk':
            print('You should enter .plk save file. Try again:')
            file_name = input()
        field = SudokuGame.__parse_game_save_file(file_name)
        if field is None:
            return None
        loaded_game = GameState(field)
        return loaded_game

    @staticmethod
    def __get_new_game_input():
        filled_cells_string = input()
        while not filled_cells_string.strip().isdigit():
            print('Wrong input. Enter an integer from [0;81]')
            filled_cells_string = input()
        return int(filled_cells_string.strip())

    @staticmethod
    def __parse_game_save_file(file_name):
        file_content = ''
        with open(file_name) as file:
            file_content = file.read()
        splitted_file = file_content.split('\n')
        if SudokuGame.__check_save_file(splitted_file):
            field = []
            for i in range(1, len(splitted_file) - 1):
                field.append(list(map(int, splitted_file[i].split(' '))))
            return field
        else:
            print('Game saves were corrupted.')
            return None

    @staticmethod
    def __check_save_file(splitted_file):
        hsh = ''
        for i in range(1, len(splitted_file)):
            if len(splitted_file[i].strip()) == 0:
                continue
            hsh += str(hashlib.md5(splitted_file[i].rstrip('\r\n').encode()).hexdigest())
        print(hsh)
        print(splitted_file[0].rstrip('\n'))
        print(len(hsh))
        print(len(splitted_file[0].rstrip('\n')))
        if splitted_file[0].rstrip('\n') == hsh:
            return True
        else:
            return False

    # Class that contains all method for field initialisation.
    class FieldCreator:

        @staticmethod
        def create_field(filled_cells_number):
            field = [[] for j in range(9)]
            field = SudokuGame.FieldCreator.add_numbers(filled_cells_number, field)
            field = SudokuGame.FieldCreator.shuffle_field(field)
            field = SudokuGame.FieldCreator.add_zeros(filled_cells_number, field)
            return field

        @staticmethod
        def add_numbers(filled_cells_number, field):
            base_line = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for i in range(3):
                for j in range(3):
                    field[i * 3 + j] = SudokuGame.FieldCreator.cyclic_shift_of_array(base_line, i + j * 3)
            return field

        @staticmethod
        def add_zeros(filled_cells_number, field):
            zero_counter = 0
            while zero_counter < 81 - filled_cells_number:
                (i, j) = (random.randrange(9), random.randrange(9))
                if field[i][j] != 0:
                    zero_counter += 1
                    field[i][j] = 0
            return field

        @staticmethod
        def cyclic_shift_of_array(array, number):
            return array[number:] + array[0:number]

        @staticmethod
        def transpose(field):
            return [[field[j][i] for j in range(len(field))] for i in range(len(field[0]))]

        @staticmethod
        def swap_rows(field):
            area_number = random.randrange(3)
            first_row = random.randrange(area_number * 3, (area_number + 1) * 3 - 1)
            second_row = random.randrange(area_number * 3, (area_number + 1) * 3 - 1)
            while first_row == second_row:
                second_row = random.randrange(area_number * 3, (area_number + 1) * 3)
            (field[first_row], field[second_row]) = (field[second_row], field[first_row])
            return field

        @staticmethod
        def swap_column(field):
            field = SudokuGame.FieldCreator.transpose(field)
            SudokuGame.FieldCreator.swap_rows(field)
            return SudokuGame.FieldCreator.transpose(field)

        @staticmethod
        def swap_row_areas(field):
            first_area_number = random.randrange(3)
            second_area_number = random.randrange(3)
            while first_area_number == second_area_number:
                second_area_number = random.randrange(3)
            for i in range(3):
                (field[first_area_number * 3 + i], field[second_area_number * 3 + i]) = \
                    (field[second_area_number * 3 + i], field[first_area_number * 3 + i])
            return field

        @staticmethod
        def swap_column_areas(field):
            field = SudokuGame.FieldCreator.transpose(field)
            SudokuGame.FieldCreator.swap_row_areas(field)
            return SudokuGame.FieldCreator.transpose(field)

        @staticmethod
        def shuffle_field(field):
            func_list = ["SudokuGame.FieldCreator.swap_rows(field)",
                         "SudokuGame.FieldCreator.transpose(field)",
                         "SudokuGame.FieldCreator.swap_column(field)",
                         "SudokuGame.FieldCreator.swap_row_areas(field)",
                         "SudokuGame.FieldCreator.swap_column_areas(field)"]
            for i in range(50):
                func_id = random.randrange(5)
                field = eval(func_list[func_id])
            return field


class GameState:

    def __init__(self, field=None):
        self.__field = field

    # Saves the game into a file.
    def save_game(self):
        save_name = 'save'
        save_duplicate_counter = 1
        while os.path.exists(save_name + '.plk'):
            save_name = 'save' + str(save_duplicate_counter)
            save_duplicate_counter += 1
        field_content = []
        for i in range(len(self.__field)):
            field_content.append(str(self.__field[i]).strip('[]').replace(',', '') + '\n')
        with open(save_name + '.plk', 'a+') as save_file:
            hsh = ''
            for line in field_content:
                hsh += str(hashlib.md5(line.rstrip('\r\n').rstrip('\n').encode()).hexdigest())
            save_file.write(str(hsh) + '\n')
            for line in field_content:
                save_file.write(line)

    def show_field(self):
        for j, line in enumerate(self.__field):
            for i, elem in enumerate(line):
                print(f"{elem} ", end='')

                if (i + 1) % 3 == 0 and i + 1 != 9:
                    print("│ ", end='')
            print()
            if (j + 1) % 3 == 0 and j + 1 != 9:
                print("──────┼───────┼──────")

    # Let player make another move.
    def make_move(self):
        return

    # Gets and parses move's command.
    def __parse_move_input(self):
        return

    # Changes cell's state.
    def __change_cell_state(self, row, column, num):
        return


game = SudokuGame.start_new_game()
game.save_game()
game = SudokuGame.load_game()
game.show_field()
