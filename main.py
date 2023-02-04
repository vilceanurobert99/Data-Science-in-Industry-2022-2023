import tkinter as tk
from itertools import combinations
from tkinter import ttk

movies = [
    {'title': 'The Shawshank Redemption', 'genres': ['Drama']},
    {'title': 'The Godfather', 'genres': ['Crime', 'Drama']},
    {'title': 'The Dark Knight', 'genres': ['Action', 'Crime', 'Drama']},
    {'title': 'The Godfather: Part II', 'genres': ['Crime', 'Drama']},
    {'title': 'The Lord of the Rings: The Return of the King', 'genres': ['Adventure', 'Drama', 'Fantasy']},
    {'title': 'Pulp Fiction', 'genres': ['Crime', 'Drama']}
]

user_ratings = [
    {'user_id': 1, 'title': 'The Shawshank Redemption', 'rating': 5},
    {'user_id': 1, 'title': 'The Godfather', 'rating': 5},
    {'user_id': 1, 'title': 'The Dark Knight', 'rating': 4},
    {'user_id': 2, 'title': 'The Shawshank Redemption', 'rating': 5},
    {'user_id': 2, 'title': 'The Godfather', 'rating': 4},
    {'user_id': 2, 'title': 'The Dark Knight', 'rating': 5},
    {'user_id': 2, 'title': 'The Godfather: Part II', 'rating': 5}
]


def mine_frequent_itemsets():
    # code to mine frequent itemsets goes here
    frequent_itemsets = {}
    for movie in movies:
        genres = movie['genres']
        for i in range(1, len(genres) + 1):
            for subset in combinations(genres, i):
                if subset in frequent_itemsets:
                    frequent_itemsets[subset] += 1
                else:
                    frequent_itemsets[subset] = 1
    frequent_itemsets = dict(filter(lambda item: item[1] >= 2, frequent_itemsets.items()))
    print("Frequent itemsets:", frequent_itemsets)


def display_itemset_length():
    itemset_length = var.get()
    itemset_data_to_display = itemset_data[itemset_length - 1]

    for itemset in itemset_data_to_display:
        print("Itemset: ", itemset[0:-1])
        print("Genres: ", itemset[-1])
        print("\n")


itemset_length_1 = [("The Shawshank Redemption", ["Drama", "Crime", "Thriller"]),
                    ("The Godfather", ["Drama", "Crime", "Thriller"]),
                    ("The Godfather: Part II", ["Drama", "Crime", "Thriller"]),
                    ("The Dark Knight", ["Action", "Crime", "Drama", "Thriller"])]

itemset_length_2 = [("The Shawshank Redemption", "The Godfather", ["Drama", "Crime", "Thriller"]),
                    ("The Shawshank Redemption", "The Godfather: Part II", ["Drama", "Crime", "Thriller"]),
                    ("The Godfather", "The Godfather: Part II", ["Drama", "Crime", "Thriller"]),
                    ("The Dark Knight", "The Shawshank Redemption",
                     ["Action", "Crime", "Drama", "Thriller", "Drama", "Crime", "Thriller"])]

itemset_length_3 = [
    ("The Shawshank Redemption", "The Godfather", "The Godfather: Part II", ["Drama", "Crime", "Thriller"]),
    ("The Dark Knight", "The Shawshank Redemption", "The Godfather",
     ["Action", "Crime", "Drama", "Thriller", "Drama", "Crime", "Thriller"])]

itemset_data = [itemset_length_1, itemset_length_2, itemset_length_3]


def all_lower(my_list):
    return [x.lower() for x in my_list]


def recommend_movie():
    # code to recommend movie based on user's input goes here
    movie = movie_entry.get()
    print("Movie:", movie)
    for m in movies:
        if m['title'].lower() == movie.lower():
            recommended_movies = []
            for g in m['genres']:
                for rm in movies:
                    if g.lower() in all_lower(rm['genres']) and all_lower(rm['title']) != movie.lower():
                        recommended_movies.append(rm['title'])
            print("Recommended movies:", recommended_movies)
            break


root = tk.Tk()
root.title("Movie Recommendation System")
root.geometry("500x500")

style = ttk.Style()
style.configure("TButton", font="Verdana 12", padding=10, background="#add8e6")
style.configure("TRadiobutton", font="Verdana 10", padding=10)
style.configure("TLabel", font="Verdana 12", padding=10)
style.configure("TEntry", font="Verdana 12", padding=10)

mine_button = ttk.Button(root, text="Start Mining", style="TButton", command=mine_frequent_itemsets)
mine_button.grid(column=0, row=0, padx=10, pady=10)

var = tk.IntVar()
var.set(1)

for i in range(1, 4):
    ttk.Radiobutton(root, text=str(i), variable=var, value=i, style="TRadiobutton",
                    command=display_itemset_length).grid(column=0, row=i)

movie_label = ttk.Label(root, text="Movie:", style="TLabel")
movie_label.grid(column=1, row=0, padx=10)

movie_entry = ttk.Entry(root, style="TEntry")
movie_entry.grid(column=2, row=0, padx=10)

recommend_button = ttk.Button(root, text="Recommend", style="TButton", command=recommend_movie)
recommend_button.grid(column=2, row=1, padx=10, pady=10)

root.mainloop()
