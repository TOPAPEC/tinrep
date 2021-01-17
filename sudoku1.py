import codecs
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
        field = None
        while len(file_name) < 5 or file_name[-4:] != '.plk':
            print('You should enter .plk save file. Try again:')
            file_name = input()
        try:
            field = SudokuGame.__parse_game_save_file(file_name)
        except Exception as ex:
            print("An error occurred while loading save: " + str(ex))
        if field is None:
            print('Unable to load the save.')
            return None
        loaded_game = GameState(field)
        print('Game is successfully loaded.')
        return loaded_game

    @staticmethod
    def run_game():
        current_game = None
        while True:
            SudokuGame.__clear_console()
            print()
            if current_game is None:
                SudokuGame.show_main_menu()
                current_game = SudokuGame.handle_main_menu_command()
            if current_game == -1:
                break
            if current_game is not None:
                while True:
                    SudokuGame.__clear_console()
                    print()
                    current_game.show_field()
                    current_game.show_help()
                    game_end_flag = current_game.handle_game_command()
                    if game_end_flag:
                        print('Terminating session...')
                        current_game = None
                        break
            input("Press Enter to continue...")

    # Doesn't work in pycharm :(
    @staticmethod
    def __clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def __get_new_game_input():
        filled_cells_string = input()
        while not filled_cells_string.strip().isdigit():
            print('Wrong input. Enter an integer from [0;81]')
            filled_cells_string = input()
        return int(filled_cells_string.strip())

    @staticmethod
    def __parse_game_save_file(file_name):
        with codecs.open(file_name, encoding='utf-8') as file:
            file_content = file.read()
        splitted_file = file_content.split('\n')
        if SudokuGame.__check_save_file(splitted_file):
            field = []
            mutable_matrix = []
            for i in range(1, 10):
                field.append(splitted_file[i].split(' '))
            # for i in range(10, len(splitted_file) - 1):
            #     mutable_matrix.append(list(map(int, splitted_file[i].split(' '))))
            # for i in range(len(field)):
            #     for j in range(len(field)):
            #         if mutable_matrix[i][j] == 1:
            #             field[i][j] = ord(field[i][j]) - ''
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
            hsh += str(hashlib.md5(splitted_file[i].strip().encode()).hexdigest())
        if splitted_file[0].strip() == hsh:
            return True
        else:
            return False

    @staticmethod
    def show_main_menu():
        print('Welcome to Sudoku game (by Topapec).')
        print('You can work with program by entering commands.')
        print('new game -- begin new game.')
        print('load -- loads a game from the file.')
        print('rules -- shows you brief rules.')
        print('exit -- exit from game.')

    @staticmethod
    def show_rules():
        print('You can see the rules of Sudoku here: https://en.wikipedia.org/wiki/Sudoku.')
        print('Bold numerals - numerals that you can change with place command.')
        print('You can check, if you won the game, only if there no zeros left.')

    @staticmethod
    def handle_main_menu_command():
        commands = ['new game', 'load', 'rules', 'exit']
        entered_command = input()
        while entered_command not in commands:
            print('Invalid command, please try again.')
            entered_command = input()
        if entered_command == commands[0]:
            return SudokuGame.start_new_game()
        elif entered_command == commands[1]:
            return SudokuGame.load_game()
        elif entered_command == commands[2]:
            SudokuGame.show_rules()
            return None
        elif entered_command == commands[3]:
            return -1

    # Class that contains all method for field initialisation.
    class FieldCreator:

        @staticmethod
        def create_field(filled_cells_number):
            field = [[] for j in range(9)]
            field = SudokuGame.FieldCreator.add_numbers(field)
            field = SudokuGame.FieldCreator.shuffle_field(field)
            field = SudokuGame.FieldCreator.add_zeros(filled_cells_number, field)
            return field

        @staticmethod
        def add_numbers(field):
            base_line = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            for i in range(3):
                for j in range(3):
                    field[i * 3 + j] = SudokuGame.FieldCreator.cyclic_shift_of_array(base_line, i + j * 3)
            return field

        @staticmethod
        def add_zeros(filled_cells_number, field):
            zero_counter = 0
            while zero_counter < 81 - filled_cells_number:
                (i, j) = (random.randrange(9), random.randrange(9))
                if field[i][j] != '𝟬':
                    zero_counter += 1
                    field[i][j] = '𝟬'
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
            field_content.append(str(self.__field[i]).strip('[]').replace(',', '').replace("'", "") + '\n')
        for line in self.__field:
            new_line = []
            for el in line:
                if ord(el) >= ord('𝟬'):
                    new_line.append('1')
                else:
                    new_line.append('0')
            field_content.append(str(new_line).strip('[]').replace(',', '').replace("'", "") + '\n')
        with open(save_name + '.plk', 'ab+') as save_file:
            hsh = ''
            for line in field_content:
                hsh += str(hashlib.md5(line.rstrip('\r\n').rstrip('\n').encode()).hexdigest())
            save_file.write((str(hsh) + '\n').encode("utf8"))
            for line in field_content:
                save_file.write(line.encode("utf8"))

        print(f"Game save successfully into the file '{save_name + '.plk'}'.")

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
        print("Enter 3 number, separated with spaces:\nrow column digit")
        inp_string = input()
        try:
            (row, column, digit) = self.__parse_move_input(inp_string)
            self.__change_cell_state(row, column, digit)
        except Exception as ex:
            print("An error occurred:\n" + str(ex))

    # Gets and parses move's command.
    def __parse_move_input(self, string):
        packed_row_column_digit = tuple(map(int, string.split()))
        if not self.__check_move_input(packed_row_column_digit):
            raise Exception("Incorrect move input. 0 <= row, column, digit < 9")
        return packed_row_column_digit

    def __check_move_input(self, packed_row_column_digit):
        (row, column, digit) = packed_row_column_digit
        if ord('0') <= ord(self.__field[row][column]) < ord('9'):
            raise Exception('You are trying to change unchangeable digit.')
        return 0 <= row < 9 and 0 <= column < 9 and 0 <= digit < 9

    # Changes cell's state.
    def __change_cell_state(self, row, column, digit):
        self.__field[row][column] = chr(ord('𝟬') + digit)

    @staticmethod
    def show_help():
        print('Available commands:')
        print('place -- allows you to place numeral in the crossing on the board.')
        print('rules -- shows the rules of the game.')
        print('save -- saves the game into file in the game\'s directory and shows the save file\'s name')
        print('check -- let you find out if you filled the field correctly.')
        print('exit -- stops current game.')

    def handle_game_command(self):
        commands = ['place', 'rules', 'save', 'check', 'exit']
        entered_command = input()
        while entered_command.split()[0] not in commands:
            print('Invalid command, please try again.')
            entered_command = input()
        if entered_command == commands[0]:
            self.make_move()
            return False
        elif entered_command == commands[1]:
            SudokuGame.show_rules()
            return False
        elif entered_command == commands[2]:
            self.save_game()
            return False
        elif entered_command == commands[3]:
            self.check_field()
            return False
        elif entered_command == commands[4]:
            return True

    def check_field(self):
        for i in range(9):
            for j in range(9):
                if self.__field[i][j] == '𝟬':
                    print('Not all cells are filled with non-zero digits, I can\'t perform this.')
                    return
        check_rows = [[0 for j in range(10)] for i in range(10)]
        check_columns = [[0 for j in range(10)] for i in range(10)]
        check_nums = [0 for i in range(10)]

    def cell_to_digit(self, cell):
        if ord('𝟬') <= ord(cell) < ord('𝟬') + 9:
            return ord(cell) - ord('𝟬');
        elif ord('0') <= ord(cell) < ord('0') + 9:
            return ord(cell) - ord('0')


SudokuGame.run_game()
