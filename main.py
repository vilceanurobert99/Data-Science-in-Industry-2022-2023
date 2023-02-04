import tkinter as tk
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
    pass


def display_itemset_length(*args):
    # code to display selected length itemset goes here
    print("Display itemset length:", var.get())


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

for i in range(1, 6):
    ttk.Radiobutton(root, text=str(i), variable=var, value=i, style="TRadiobutton",
                    command=display_itemset_length).grid(column=0, row=i)

movie_label = ttk.Label(root, text="Movie:", style="TLabel")
movie_label.grid(column=1, row=0, padx=10)

movie_entry = ttk.Entry(root, style="TEntry")
movie_entry.grid(column=2, row=0, padx=10)

recommend_button = ttk.Button(root, text="Recommend", style="TButton", command=recommend_movie)
recommend_button.grid(column=2, row=1, padx=10, pady=10)

root.mainloop()
