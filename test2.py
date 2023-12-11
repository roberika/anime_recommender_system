##k = 20
##cols = [("-" + str(i) + "-" + str(j)) for j in ["i", "d"] for i in range(1, k+1)]
##print(cols)

# Initialisasi package
# Database Phase
import pandas as pd
import pickle
import numpy as np
from scipy.sparse import csr_matrix
from pandas.api.types import CategoricalDtype
import sklearn
from sklearn.neighbors import NearestNeighbors
# Visualization Phase
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import math
import matplotlib.pylab as pylab
pd.set_option('display.max_columns', 500)
mpl.style.use('ggplot')
sns.set_style('white')
pylab.rcParams['figure.figsize'] = 12,8
# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

def load_anime_data():
    return pd.read_csv("dataset/anime.csv")
full_anime_data = load_anime_data()
print(full_anime_data.shape)

def create_anime_dictionary():
    pd.set_option("display.max_colwidth", None)
    s = "class AnimeDictionary {\nconst animeDictionary = {\n"
    full_anime_data["Code"] = '"' + full_anime_data["MAL_ID"].astype(str) + '": "' + full_anime_data["Name"].str.replace('"', '', regex=False) + '",\n'
    s += ''.join(full_anime_data["Code"].to_list())
    s += "}\n}\n"
    print(s)
    with open(r'anime_dictionary.dart', 'a', encoding="utf-8") as f:
        f.write(s)
    f.close()
create_anime_dictionary()







