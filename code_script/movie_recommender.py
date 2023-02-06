'''
@author: solomon
'''


import pandas as pd
from code_script.apriori import Apriori, Runner


class MovieRecommender(object):
    def __init__(self):
        self.runner = Runner()

    def recommend_movie(self, movie_list=None):
        rules_df, _ = self.runner.get_rules()
        rules_df['antecedents_list'] = rules_df['antecedents'].apply(lambda x: list(x))
        rules_df['consequents_list'] = rules_df['consequents'].apply(lambda x: list(x))
        # print(rules_df)

        rules_df['recommend'] = rules_df['antecedents_list'].apply(lambda x: 1 if set(movie_list).issubset(set(x)) else 0)
        recommend_movies = rules_df[rules_df['recommend'] == 1]
        recommend_movies.sort_values(by=['confidence'], ascending=False, inplace=True)
        recommend_movies.drop_duplicates(subset=['consequents_list'], keep='first', inplace=True)
        # print(recommend_movies)

        movies_list = recommend_movies[['confidence', 'consequents_list']].values.tolist()
        if movies_list:
            confidence = movies_list[0][0]
            movie = movies_list[0][1][0]

            print(movie + ' ' + str(confidence))

            return movie, confidence#, movie_list[:3]
        else:
            print('No movie found to recommend...')

            return 0
        # print(movies_list)


def main():
    movie_list = ['Ant-Man and the Wasp', 'Spider-Man: Far from Home']

    movie_recommender = MovieRecommender()
    movie_recommender.recommend_movie(movie_list)


if __name__ == '__main__':
    main()