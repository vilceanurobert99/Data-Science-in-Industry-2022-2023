'''
@author: solomon
@date: 28-01-2023
'''


from PickleLoader import PickleStore


class DataLoad(object):
    def __init__(self, path, lines=0):
        self.path = path
        self.lines = lines

    def transactional_data_set(self):
        transactions = []
        with open(self.path, "r") as file:
            if self.lines > 0:
                for index, line in enumerate(file):
                    if index+1 > self.lines:
                        break
                    transaction = line.strip().split(";")
                    transactions.append(set(transaction))
            else:
                for index, line in enumerate(file):
                    transaction = line.strip().split(";")
                    transactions.append(set(transaction))

        return transactions

    def transactional_data_list(self):
        transactions = []
        with open(self.path, "r") as file:
            if self.lines > 0:
                for index, line in enumerate(file):
                    if index+1 > self.lines:
                        break
                    transaction = line.strip().split(";")
                    transactions.append(list(transaction))
            else:
                for line in file:
                    transaction = line.strip().split(";")
                    transactions.append(list(transaction))

        return transactions


def main():
    # only for 2 lines
    file_path = r'/dataset/movies.txt'
    data_load = DataLoad(file_path, 500)

    transactions = data_load.transactional_data_list()
    print(transactions)

    file_path = r'/data/transactional_data_sample_500_list'
    pickle_store = PickleStore()
    pickle_store.write_list(file_path, transactions)


    # For whole document
    # file_path = r'C:/Users/Andrei/OneDrive/Documents/GitHub/Data-Science-in-Industry-2022-2023/dataset/movies.txt'
    # data_load = DataLoad(file_path)
    #
    # transactions = data_load.transactional_data_set()
    # print(transactions)
    # print(len(transactions))
    #
    # file_path = r'C:/Users/Andrei/OneDrive/Documents/GitHub/Data-Science-in-Industry-2022-2023/data/transactional_data_set'
    # pickle_store = PickleStore()
    # pickle_store.write_list(file_path, transactions)


if __name__ == '__main__':
    main()