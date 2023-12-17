import pandas as pd
import pickle
import numpy as np

def load_anime_data():
    return pd.read_csv("dataset/anime.csv")
full_anime_data = load_anime_data()
print(full_anime_data.shape)

names = full_anime_data[["MAL_ID", "Name"]].set_index("MAL_ID")
pickle.dump(names, open('names.sav', 'wb'))

