# Class that helps us store data about every single state of share price.
class ShareState:

    def __init__(self, row='0,0,0,0'):
        (self.date, self.price, self.time) = self.convert_row(row)

    # This function parses our table's row into 3 variables.
    @staticmethod
    def convert_row(row):
        splitted_row = row.split(',')[1:]
        (date, time, price) = map(ShareState.apply_rstrip, tuple(splitted_row))
        (date, time) = map(int, (date, time))
        price = float(price)
        return date, price, time

    @staticmethod
    def apply_rstrip(string):
        return string.rstrip('\n')


# This class let us store info about 1 transaction + link to the transaction made before it.
class TransactionInfo:
    def __init__(self, ss1=ShareState(), ss2=ShareState()):
        self.profit = ss2.price - ss1.price
        self.share_state1 = ss1
        self.share_state2 = ss2
        self.total_profit = self.profit
        self.prev_trans = None

    def add_prev_trans(self, prev_trans):
        self.prev_trans = prev_trans
        self.total_profit = self.profit + self.prev_trans.total_profit


# The main idea of this solution is that we can reduce total amount of share cost points.
# We can set constant delta. We go from beginning of input data to its end.
# Whenever absolute value of last remembered point's price minus
# price of point we are standing on is greater than delta, we put the current point into the compressed_lst and its
# share price value into the compressed_lst_nums. This way we compress total number of points several times.
# Now we can find the best solution with dynamic algorithm.
# dp[i][j] - the Transaction object a, a.total_profit - best possible profit with i transactions on
# first j points of lst (compressed input data).
# dp[i][j] = max(dp[i][j-1], max(dp[i-1][f] + compressed_list[j] - compressed_list[f])) where
# f belongs to [0,j-1].
# Also speed of program can be increased by increasing delta value (it will also decrease accuracy of solution).
class Solution3:
    lst = []
    lst_nums = []
    compressed_list = []
    compressed_list_nums = []
    delta = 7

    @staticmethod
    def parse_file(file_name):
        with open(file_name) as file:
            next(file)
            for row in file.readlines():
                Solution3.lst.append(ShareState(row))
                Solution3.lst_nums.append(float(row.split(',')[3]))

    @staticmethod
    def compress_input_data():
        last_elem = Solution3.lst_nums[0]
        for i in range(len(Solution3.lst)):
            if abs(last_elem - Solution3.lst_nums[i]) >= Solution3.delta:
                last_elem = Solution3.lst_nums[i]
                Solution3.compressed_list.append(Solution3.lst[i])
                Solution3.compressed_list_nums.append(Solution3.lst_nums[i])

    @staticmethod
    def k_interval_strategy_get_transaction_history():
        print('Enter the k value (should be a positive integer). k - the desired number of intervals in the strategy:')
        k = int(input())
        dp = [[TransactionInfo() for j in range(len(Solution3.compressed_list_nums))] for i in range(k + 1)]
        for i in range(1, k + 1):
            for j in range(1, len(Solution3.compressed_list_nums)):
                if j % 1000 == 0:
                    # Completion rate is not really accurate, but in general it shows the progress.
                    completion_rate = \
                        ((i - 1) * len(Solution3.compressed_list) + j) / len(Solution3.compressed_list) / k * 100
                    print(f"{completion_rate:.2f}% is done")
                best_trans_ij = dp[i][j - 1]
                for f in range(j):
                    trans_fj = TransactionInfo(Solution3.compressed_list[f], Solution3.compressed_list[j])
                    if dp[i - 1][f].total_profit + trans_fj.profit > best_trans_ij.total_profit:
                        best_trans_ij = trans_fj
                        best_trans_ij.add_prev_trans(dp[i - 1][f])
                dp[i][j] = best_trans_ij
        return Solution3.get_array_of_transaction_history(dp[k][len(Solution3.compressed_list) - 1])

    @staticmethod
    def get_array_of_transaction_history(last_transaction):
        current_transaction = last_transaction
        trans_history = []
        while current_transaction.total_profit != 0:
            trans_history.append(current_transaction)
            current_transaction = current_transaction.prev_trans
        return trans_history

    @staticmethod
    def get_money_amount_and_print_strategy(transaction_history):
        print("Enter the amount of money you have:")
        start_money = int(input())
        current_money = start_money
        for i, transaction in enumerate(transaction_history):
            print(f"In the {i + 1}'th round:")
            print(f"You have {current_money:.2f}.")
            print(
                f"You buy {int(current_money / transaction.share_state1.price)}"
                f" shares for {transaction.share_state1.price:.2f} each.")
            print(f"You sell them for {transaction.share_state2.price:.2f} each."
                  f" You get "
                  f"{(current_money / transaction.share_state1.price) * transaction.share_state2.price:.2f} profit.")
            current_money = current_money % transaction.share_state1.price + int(
                current_money / transaction.share_state1.price) * transaction.share_state2.price
            print(f"Now you have {current_money:.2f}.")
        after_transactions_money = current_money
        print(f"Your total profit is {after_transactions_money - start_money:.2f}.")
        
    # This method executes the whole solution.
    @staticmethod
    def print_solution(filename):
        Solution3.parse_file(filename)
        Solution3.compress_input_data()
        Solution3.get_money_amount_and_print_strategy(Solution3.k_interval_strategy_get_transaction_history())


Solution3.print_solution('new.csv')
