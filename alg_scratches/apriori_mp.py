import itertools
import multiprocessing as mp
from collections import defaultdict
from code_script.PickleLoader import PickleStore
import time


class Apriori(object):
    def __init__(self, transactions, min_support, min_confidence):
        self.transactions = transactions
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.itemsets = defaultdict(int)
        self.rules = []

    def _get_combinations(self, items):
        mylist= [itemset for i in range(1, len(items)+1) for itemset in itertools.combinations(items, i)]
        myset = set(mylist)
        mylist = list(myset)

        return mylist

    # def _get_combinations(self, items):
    #     def gray_code(n):
    #         if n == 0:
    #             yield []
    #         else:
    #             for subset in gray_code(n - 1):
    #                 yield subset
    #                 yield subset + [n - 1]
    #
    #     return [itemset for i in range(1, len(items) + 1) for itemset in gray_code(len(items)) if len(itemset) == i]

    # def _get_combinations(self, items):
    #     for i in range(1, len(items) + 1):
    #         for itemset in itertools.combinations(items, i):
    #             yield itemset

    # def _get_combinations(self, items):
    #     n = len(items)
    #     for i in range(1 << n):
    #         yield [items[j] for j in range(n) if (i & (1 << j))]

    # def _get_combinations(self, items):
    #     return list((itemset for i in range(1, len(items) + 1) for itemset in itertools.combinations(items, i)))

    def _get_frequent_itemsets(self, itemsets, chunk_start, chunk_end):
        frequent_itemsets = defaultdict(int)
        for transaction in self.transactions[chunk_start:chunk_end]:
            for itemset in itemsets:
                if set(itemset).issubset(set(transaction)):
                    frequent_itemsets[itemset] += 1
        return frequent_itemsets

    def _generate_association_rules(self, itemsets):
        for itemset in itemsets:
            for item in set(itemset):
                antecedent = (item,)
                consequent = tuple(set(itemset) - set(antecedent))
                confidence = itemsets[itemset] / itemsets[antecedent]
                if confidence >= self.min_confidence:
                    self.rules.append((antecedent, consequent, confidence))

    def fit(self, n_jobs=1):
        items = set().union(*self.transactions)
        itemsets = self._get_combinations(items)
        # print(itemsets)

        if n_jobs == 1:
            frequent_itemsets = self._get_frequent_itemsets(itemsets, 0, len(self.transactions))
        else:
            pool = mp.Pool(n_jobs)
            chunk_size = len(self.transactions) // n_jobs
            chunks = [(chunk_size * i, chunk_size * (i + 1)) for i in range(n_jobs - 1)] + [(chunk_size * (n_jobs - 1), len(self.transactions))]
            results = pool.starmap(self._get_frequent_itemsets, [(itemsets, start, end) for start, end in chunks])
            frequent_itemsets = defaultdict(int)
            k = 1
            print(len(results))
            for result in results:
                print(k)
                k += 1
                for itemset, count in result.items():
                    frequent_itemsets[itemset] += count

        self.itemsets = {itemset: count for itemset, count in frequent_itemsets.items() if count >= self.min_support}
        self._generate_association_rules(self.itemsets)

    def get_itemsets(self):
        return self.itemsets

    def get_rules(self):
        return self.rules


def main():
    file_path = r'C:/Users/Andrei/OneDrive/Documents/GitHub/Data-Science-in-Industry-2022-2023/data/transactional_data_sample_100_set'
    pickle_store = PickleStore()
    transactional_sample_dataset = pickle_store.read_list(file_path)

    apriori = Apriori(transactional_sample_dataset, min_support=3, min_confidence=0.6)
    start = time.time()
    apriori.fit(n_jobs=6)
    end = time.time()

    print("Elapsed time using process_time()", (end - start) * 10 ** 3, "ms.")

    frequent_itemsets = apriori.get_itemsets()
    print("Frequent itemsets:")
    for itemset, count in frequent_itemsets.items():
        print(f"{itemset}: {count}")

    association_rules = apriori.get_rules()
    print("\nAssociation rules:")
    for antecedent, consequent, confidence in association_rules:
        print(f"{antecedent} -> {consequent}: {confidence:.2f}")


if __name__ == '__main__':
    main()