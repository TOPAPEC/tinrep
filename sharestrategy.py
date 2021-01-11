# This file contains all 3 solutions for task 1 from programming.

class ShareState:

    def __init__(self, row):
        (self.date, self.price, self.time) = self.convert_row(row)

    # This function parses our table's row into 3 variables.
    @staticmethod
    def convert_row(row):
        splitted_row = row.split(',')
        (index, date, time, price) = map(ShareState.apply_rstrip, tuple(splitted_row))
        (date, time) = map(int, (date, time))
        price = float(price)
        return date, price, time

    @staticmethod
    def apply_rstrip(string):
        return string.rstrip('\n')


# First strategy.
# Let's generate an array, where a[i] - minimal element from a[0]
# to a[i] and i - number of entry in table.
# Then we will walk through the lines of the table and find the maximum
# f - a[j], where j - number of entry in the table, f - price of the
# share from that entry.
class FirstSolution:
    @staticmethod
    def generate_minarray(file_name):
        a = []
        with open(file_name) as file:
            next(file)
            for index, row in enumerate(file.readlines()):
                # We can't trust index from table because it becomes zero at
                # the beginning of every new year.
                current_share_state = ShareState(row)
                if index == 0:
                    a.append(current_share_state)
                    continue
                previous_min_share_state = a[index - 1]
                if current_share_state.price < previous_min_share_state.price:
                    a.append(current_share_state)
                else:
                    a.append(previous_min_share_state)
        return a

    # Here we are walking through the whole table to find the max profit
    # transaction.
    @staticmethod
    def one_transaction_strategy(file_name):
        a = FirstSolution.generate_minarray(file_name)
        buy_day = []
        sell_day = []
        with open(file_name) as file:
            next(file)
            maximum_profit = 0
            for index, row in enumerate(file.readlines()):
                current_share_state = ShareState(row)
                min_share_state = a[index]
                if index == 0:
                    continue
                if current_share_state.price - min_share_state.price > maximum_profit:
                    buy_day = min_share_state
                    sell_day = current_share_state
                    maximum_profit = current_share_state.price - min_share_state.price
        return buy_day, sell_day

    @staticmethod
    def solve_and_print_solution(file_name):
        (buy_day, sell_day) = FirstSolution.one_transaction_strategy(file_name)
        print(f'You buy shares at {buy_day.date} {buy_day.time} with price {buy_day.price}')
        print(f'And sell them at {sell_day.date} {sell_day.time} with price {sell_day.price}')
        print(f'Your profit will be {sell_day.price - buy_day.price} per share')


FirstSolution.solve_and_print_solution('new.csv')


# Second strategy.
# We generate the same min array.
# Also we generate min array for reversed input list.
# Then we are beginning to iterate through list. Our index - separate point for array.
# On the left side from it we find left optimal interval (O(1)).
# The same on the right side (with help of min array for reversed list). 
# On the left side we are saving most profitable interval.
# On the right side we are forced to update interval every time separate point changes,
# because separate point there goes from right to left, but min array is calculated from left to right.
class SecondSolution:
    list = []
    reversed_list = []
    min_array = []
    reversed_min_array = []

    # Parses all elements from file_name into list and reversed_list.
    @staticmethod
    def parse_file(file_name):
        with open(file_name) as file_input:
            next(file_input)
            for row in file_input:
                SecondSolution.list.append(ShareState(row))
        SecondSolution.reversed_list = SecondSolution.list[:]
        SecondSolution.reversed_list.reverse()

    # Create array a, where a[i] - element with minimal price in range [0;i].
    @staticmethod
    def create_min_array(array):
        min_array = []
        for index, state in enumerate(array):
            if index == 0:
                min_array.append(state)
                continue
            prev_min = min_array[index - 1]
            if prev_min.price > state.price:
                min_array.append(state)
            else:
                min_array.append(prev_min)
        return min_array

    # Returns ShareState objects that are limits of optimal intervals with exact separate points.
    @staticmethod
    def get_intervals(point_of_separation):
        index_left = point_of_separation
        index_right = len(SecondSolution.reversed_list) - 1 - point_of_separation
        left_min = SecondSolution.min_array[index_left]
        right_min = SecondSolution.reversed_min_array[index_right]
        left_cur = SecondSolution.list[index_left]
        right_cur = SecondSolution.reversed_list[index_right]
        return left_min, left_cur, right_min, right_cur

    # Just returns total profit from 2 transactions on this intervals.
    @staticmethod
    def get_sum_of_intervals(interval1_start, interval1_end, interval2_start, interval2_end):
        return (interval1_end.price - interval1_start.price) + (interval2_end.price - interval2_start.price)
    # Iterates through list and searches for best solution.
    @staticmethod
    def two_transaction_strategy():
        best_intervals_sum = 0
        best_intervals_limits = (None, None, None, None)
        max_left_interval_sum = 0
        max_left_interval_limits = (None, None)
        for index in range(len(SecondSolution.list)):
            left_min, left_max, right_min, right_max = SecondSolution.get_intervals(index)
            if left_max.price - left_min.price > max_left_interval_sum or max_left_interval_sum == 0:
                max_left_interval_sum = left_max.price - left_min.price
                max_left_interval_limits = (left_min, left_max)
            current_interval_sum = SecondSolution. \
                get_sum_of_intervals(*max_left_interval_limits, right_min, right_max)
            if current_interval_sum > best_intervals_sum:
                best_intervals_sum = current_interval_sum
                best_intervals_limits = (*max_left_interval_limits, right_min, right_max)
        return best_intervals_limits
    # Runs several functions to get solution then prints it in readable form.
    @staticmethod
    def solve_and_print_solution(file_name):
        SecondSolution.parse_file(file_name)
        SecondSolution.min_array = SecondSolution.create_min_array(SecondSolution.list)
        SecondSolution.reversed_min_array = SecondSolution.create_min_array(SecondSolution.reversed_list)
        (left_min, left_max, right_min, right_max) = SecondSolution.two_transaction_strategy()
        print(f'The first time you buy the shares at {left_min.date} {left_min.time} with price {left_min.price},')
        print(f'then you sell them at {left_max.date} {left_max.time} with price {left_max.price}.')
        print(f'The second time you buy the shares at {right_min.date} {right_min.time} with price {right_min.price},')
        print(f'then you sell them at {right_max.date} {right_max.time} with price {right_max.price}.')
        print(f'You get {left_max.price - left_min.price} per share in first transaction and')
        print(f'you get {right_max.price - right_min.price} per share in second transaction.')


SecondSolution.solve_and_print_solution('new.csv')
