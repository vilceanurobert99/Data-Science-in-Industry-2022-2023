'''
@author: solomon
'''


import numpy as np
import pandas as pd
from itertools import combinations


class Apriori(object):
    def __init__(self):
        pass

    def apriori(self, df, min_support=0.05):
        if min_support <= 0.0:
            raise ValueError(
                "0 < Support <= 1"
            )

        X = df.values
        support = self._support(X, X.shape[0])
        absolute_support = self._absolute_support(X, X.shape[0])
        ary_col_idx = np.arange(X.shape[1])
        support_dict = {1: support[support >= min_support]}
        absolute_support_dict = {1: absolute_support}
        itemset_dict = {1: ary_col_idx[support >= min_support].reshape(-1, 1)}
        max_itemset = 1
        rows_count = float(X.shape[0])

        # all_ones = np.ones((int(rows_count), 1))

        while max_itemset and max_itemset < (float("inf")):
            next_max_itemset = max_itemset + 1
            combin = self.generate_new_combinations(itemset_dict[max_itemset])
            combin = np.fromiter(combin, dtype=int)
            combin = combin.reshape(-1, next_max_itemset)

            if combin.size == 0:
                break

            _bools = np.all(X[:, combin], axis=2)

            support = self._support(np.array(_bools), rows_count)
            absolute_support = self._absolute_support(np.array(_bools), rows_count)
            _mask = (support >= min_support).reshape(-1)
            if any(_mask):
                itemset_dict[next_max_itemset] = np.array(combin[_mask])
                support_dict[next_max_itemset] = np.array(support[_mask])
                absolute_support_dict[next_max_itemset] = np.array(absolute_support[_mask])
                max_itemset = next_max_itemset
            else:
                break

        all_res = []
        for k in sorted(itemset_dict):
            support = pd.Series(support_dict[k])
            absolute_support = pd.Series(absolute_support_dict[k])
            itemsets = pd.Series([frozenset(i) for i in itemset_dict[k]], dtype="object")

            res = pd.concat((support, absolute_support, itemsets), axis=1)
            all_res.append(res)

        res_df = pd.concat(all_res)
        res_df.columns = ["support", "absolute_support", "itemsets"]

        mapping = {idx: item for idx, item in enumerate(df.columns)}
        res_df["itemsets"] = res_df["itemsets"].apply(
            lambda x: frozenset([mapping[i] for i in x])
        )

        res_df = res_df.reset_index(drop=True)

        return res_df

    def _support(self, _x, _number_of_rows):
        res = np.sum(_x, axis=0) / _number_of_rows
        return np.array(res).reshape(-1)

    def _absolute_support(self, _x, _number_of_rows):
        res = np.sum(_x, axis=0)
        return np.array(res).reshape(-1)

    def generate_new_combinations(self, old_combinations):
        items_types_in_previous_step = np.unique(old_combinations.flatten())
        for old_combination in old_combinations:
            max_combination = old_combination[-1]
            mask = items_types_in_previous_step > max_combination
            valid_items = items_types_in_previous_step[mask]
            old_tuple = tuple(old_combination)

            for item in valid_items:
                yield from old_tuple
                yield item

    def association_rules(self, df, min_confidence=0.8):
        if not df.shape[0]:
            raise ValueError(
                "Dataframe is empty"
            )

        to_compute = "confidence"

        metric_dict = {
            "antecedent support": lambda _, antecedent_support, __: antecedent_support,
            "consequent support": lambda _, __, consequent_support: consequent_support,
            "support": lambda support, _, __: support,
            "confidence": lambda support, antecedent_support, _: support / antecedent_support
        }

        columns_ordered = [
            "antecedent support",
            "consequent support",
            "support",
            "confidence"
        ]

        keys = df["itemsets"].values
        values = df["support"].values
        frozenset_vect = np.vectorize(lambda x: frozenset(x))
        frequent_items_dict = dict(zip(frozenset_vect(keys), values))

        rule_antecedents = []
        rule_consequents = []
        rule_supports = []

        for k in frequent_items_dict.keys():
            support = frequent_items_dict[k]
            for idx in range(len(k) - 1, 0, -1):
                for c in combinations(k, r=idx):
                    antecedent = frozenset(c)
                    consequent = k.difference(antecedent)

                    antecedent_support = frequent_items_dict[antecedent]
                    consequent_support = frequent_items_dict[consequent]

                    score = metric_dict[to_compute](support, antecedent_support, consequent_support)
                    if score >= min_confidence:
                        rule_antecedents.append(antecedent)
                        rule_consequents.append(consequent)
                        rule_supports.append([support, antecedent_support, consequent_support])

        if not rule_supports:
            return pd.DataFrame(columns=["antecedents", "consequents"] + columns_ordered)

        else:
            rule_supports = np.array(rule_supports).T.astype(float)
            df_res = pd.DataFrame(
                data=list(zip(rule_antecedents, rule_consequents)),
                columns=["antecedents", "consequents"],
            )

            support = rule_supports[0]
            antecedent_support = rule_supports[1]
            consequent_support = rule_supports[2]
            for m in columns_ordered:
                df_res[m] = metric_dict[m](support, antecedent_support, consequent_support)

            return df_res


class Runner(object):
    def __init__(self):
        self.file_path = r'C:/Users/Andrei/OneDrive/Documents/GitHub/Data-Science-in-Industry-2022-2023/dataset/movies.csv'

    def get_rules(self):
        data = pd.read_csv(self.file_path)

        apriori = Apriori()
        frequent_itemsets = apriori.apriori(data, min_support=0.05)
        rules = apriori.association_rules(frequent_itemsets, min_confidence=0.5)

        return rules, frequent_itemsets

    def write_rules(self):
        association_rules_output = r'C:/Users/Andrei/OneDrive/Documents/GitHub/Data-Science-in-Industry-2022-2023/dataset/association_rules.csv'
        rules, _ = self.get_rules()

        rules.to_csv(association_rules_output, encoding='utf-8', index=False)

    def write_frequent_itemsets(self):
        association_rules_output = r'C:/Users/Andrei/OneDrive/Documents/GitHub/Data-Science-in-Industry-2022-2023/dataset/frequent_itemset.csv'
        _, frequent_itemsets = self.get_rules()

        frequent_itemsets.to_csv(association_rules_output, encoding='utf-8', index=False)

    def get_single_item(self):
        data = pd.read_csv(self.file_path)

        apriori = Apriori()
        frequent_itemsets = apriori.apriori(data, min_support=0.05)
        frequent_itemsets['filter'] = frequent_itemsets['itemsets'].apply(lambda x: len(x) > 1)

        frequent_solo = frequent_itemsets[frequent_itemsets['filter'] == False]
        frequent_solo['item'] = frequent_solo['itemsets'].apply(lambda x: list(x))
        frequent_solo['out'] = frequent_solo.apply(lambda x: str(x['absolute_support']) + ':' + x['item'][0], axis=1)
        frequent_solo.sort_values(by=['absolute_support'], ascending=True, inplace=True)
        frequent_item_list = frequent_solo['out'].values.tolist()

        return frequent_item_list

    def write_single_item(self):
        frequent_item_output_text_file = r'C:/Users/Andrei/OneDrive/Documents/GitHub/Data-Science-in-Industry-2022-2023/dataset/frequent_item.txt'
        frequent_item_list = self.get_single_item()

        with open(frequent_item_output_text_file, 'w') as f:
            for item in frequent_item_list:
                f.write(item + "\n")

    def get_multiple_itemsets(self):
        data = pd.read_csv(self.file_path)

        apriori = Apriori()
        frequent_itemsets = apriori.apriori(data, min_support=0.05)
        frequent_itemsets['filter'] = frequent_itemsets['itemsets'].apply(lambda x: len(x) > 1)

        frequent_multiple = frequent_itemsets[frequent_itemsets['filter'] == True]
        frequent_multiple['item'] = frequent_multiple['itemsets'].apply(lambda x: ';'.join(list(x)))
        frequent_multiple['out'] = frequent_multiple.apply(lambda x: str(x['absolute_support']) + ':' + x['item'],
                                                           axis=1)
        frequent_multiple.sort_values(by=['absolute_support'], ascending=True, inplace=True)
        frequent_itemsets_list = frequent_multiple['out'].values.tolist()

        return frequent_itemsets_list

    def write_multiple_itemsets(self):
        frequent_itemsets_output_text_file = r'C:/Users/Andrei/OneDrive/Documents/GitHub/Data-Science-in-Industry-2022-2023/dataset/frequent_itemsets.txt'
        frequent_itemsets_list = self.get_multiple_itemsets()

        with open(frequent_itemsets_output_text_file, 'w') as f:
            for indx, item in enumerate(frequent_itemsets_list):
                if indx < len(frequent_itemsets_list)-1:
                    f.write(item + "\n")
                else:
                    f.write(item)


def main():
    run = Runner()
    run.get_rules()


if __name__ == '__main__':
    main()