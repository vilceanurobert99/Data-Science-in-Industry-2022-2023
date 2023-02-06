import customtkinter
from code_script.apriori import Runner
from code_script.movie_recommender import MovieRecommender
import re


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Mine frequent movies")
        self.geometry(f"{1100}x{450}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="MovieRecommender", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250, height=350)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Settings")
        self.tabview.add("Recommender")
        self.tabview.tab("Settings").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

        self.tabview.tab("Recommender").grid_columnconfigure(0, weight=1)
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Settings"), dynamic_resizing=False,
                                                        values=["Single item", "Multiple itemsets"], command=self.callback)
        self.optionmenu_1.grid(row=0, column=0, padx=50, pady=(20, 10))

        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Recommender"), text="Insert movie/s to make a recommendation")

        self.entry = customtkinter.CTkEntry(self.tabview.tab("Recommender"), placeholder_text="Movie list")
        self.entry.grid(row=3, padx=(5, 0), pady=(20, 0), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self.tabview.tab("Recommender"), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                     text='Recommend', command=self.recommend_movie)
        self.main_button_1.grid(row=4, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("Mining type")
        self.textbox.insert("0.0", "Movie list\n")

    def recommend_movie(self):
        movie_list = list(re.split(', |,|;|; ', self.entry.get()))
        print(movie_list)

        movie_recommender = MovieRecommender()
        _movie = movie_recommender.recommend_movie(movie_list)
        if _movie != 0:
            movie, confidence = movie_recommender.recommend_movie(movie_list)
            _print_movie = 'We recommend you: {} - {}% confidence\n'.format(movie, int(confidence * 100))
            print('We recommend you: {} - {}'.format(movie, confidence))
            self.textbox.delete("1.0", "end")
            self.textbox.insert("0.0", _print_movie + "\n")
            # _print_movie = ''
            # for _movie in _rlist:
            #     r_movie = _movie[1][0]
            #     r_confidence = _movie[0]
            #     _print_movie = 'We recommend you: {} - {}% confidence'.format(r_movie, int(r_confidence * 100))
            #     self.textbox.insert("0.0", _print_movie + "\n")
        else:
            print('No movie found to recommend!')
            self.textbox.delete("1.0", "end")
            self.textbox.insert("0.0", 'No movie found to recommend!' + "\n")


    def callback(self, selection):
        runner = Runner()
        single_item_list = runner.get_single_item()
        multiple_itemset_list = runner.get_multiple_itemsets()

        print(selection)
        self.textbox.delete("1.0", "end")

        if selection == 'Single item':
            self.textbox.delete("1.0", "end")
            for item in single_item_list:
                self.textbox.insert("0.0", str(item) + "\n")
        elif selection == 'Multiple itemsets':
            self.textbox.delete("1.0", "end")
            for item in multiple_itemset_list:
                self.textbox.insert("0.0", str(item) + "\n")


    def open_input_dialog_event(self):
        _input = self.callback()
        print("CTkInputDialog:", _input)
        self.textbox.delete("1.0", "end")
        self.textbox.insert("0.0", str(_input))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
