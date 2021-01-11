
class ShareState:
    date = 0
    price = 0
    time = 0

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
    def generate_minarray(filename):
        a = []
        with open(filename) as file:
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
    def one_transaction_strategy(filename):
        a = FirstSolution.generate_minarray(filename)
        buy_day = []
        sell_day = []
        with open(filename) as file:
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
    def print_solution(filename):
        (buy_day, sell_day) = FirstSolution.one_transaction_strategy(filename)
        print(f'You buy shares at {buy_day.date} {buy_day.time} with price {buy_day.price}')
        print(f'And sell them at {sell_day.date} {sell_day.time} with price {sell_day.price}')
        print(f'Your profit will be {sell_day.price - buy_day.price} per share')


FirstSolution.print_solution('new.csv')

# Second strategy.
# We generate the same min array.
# Then we generate two more.
# The first one: a[i] - minimal element in range
class SecondSolution:
    @staticmethod
    def generate_min_array(filename):
        a = []
        with open(filename) as file:
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

    @staticmethod
    def generate_max_array(filename):
