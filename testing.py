import pandas as pd
import pickle
import numpy as np
from scipy.sparse import csr_matrix
from pandas.api.types import CategoricalDtype
import sklearn
from sklearn.neighbors import NearestNeighbors
import math
pd.set_option('display.max_columns', 500)

def load_anime_data():
    return pd.read_csv("dataset/anime.csv")
full_anime_data = load_anime_data()
print(full_anime_data.shape)

def load_rating_data():
    return pd.read_csv("dataset/filtered_rating_data.csv")
rating_data = load_rating_data()
print(rating_data.shape)

def get_anime(rating_data):
    return rating_data.anime_id.drop_duplicates()
anime_data = get_anime(rating_data)

def get_users(rating_data):
    return rating_data.user_id.drop_duplicates()
user_data = get_users(rating_data)

def print_data_count():
    print("Number of anime  : ", len(anime_data))
    print("Number of users  : ", rating_data['user_id'].max())
    print("Number of ratings: ", len(rating_data))
print_data_count()

def create_model():
    print("Separating user")
    
    print("Intializing row and columns...")
    anime_c = CategoricalDtype(sorted(full_anime_data.MAL_ID.unique()))
    user_c = CategoricalDtype(sorted(rating_data.user_id.unique()))
    row = rating_data.anime_id.astype(anime_c).cat.codes
    col = rating_data.user_id.astype(user_c).cat.codes
    rating_data["one"] = 1

    print("Creating scipy sparse matrix...")
    watch_data = csr_matrix((rating_data["one"], (row, col)), shape=(anime_c.categories.size, user_c.categories.size))

    print("Converting scipy sparse matrix to pandas sparse DataFrame...")
    watch_data = pd.DataFrame.sparse.from_spmatrix(watch_data, index=anime_c.categories, columns=user_c.categories).fillna(0)

    print("Creating Nearest Neighbors model...")
    distance_model = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    distance_model.fit(watch_data)


