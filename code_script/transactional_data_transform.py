import pandas as pd


def preprocess(file):
    with open(file) as f:
        lines = f.readlines()
        # lines = f.readlines(1024)

    transactions = []
    items = set()

    for line in lines:
        transaction = line.strip().split(';')
        transactions.append(transaction)
        items.update(transaction)

    items = list(items)
    item_index = {item: index for index, item in enumerate(items)}
    data = []

    for transaction in transactions:
        row = [0] * len(items)
        for item in transaction:
            index = item_index[item]
            row[index] = 1
        data.append(row)

    data = pd.DataFrame(data, columns=items)

    return data

data = preprocess(r'/dataset/movies.txt')
print(data)
data.to_csv(r'C:/Users/Andrei/OneDrive/Documents/GitHub/Data-Science-in-Industry-2022-2023/dataset/movies.csv', encoding='utf-8', index=False)
# data.to_csv(r'C:/Users/Andrei/OneDrive/Documents/GitHub/Data-Science-in-Industry-2022-2023/dataset/movies_500.csv', encoding='utf-8', index=False)
