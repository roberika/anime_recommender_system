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

def get_users(rating_data):
    return rating_data.user_id.drop_duplicates()
user_data = get_users(rating_data)

def print_data_count():
    print("Number of anime  : ", len(full_anime_data))
    print("Number of users  : ", len(rating_data.user_id.unique()))
    print("Number of ratings: ", len(rating_data))
##    t = rating_data.set_index(["user_id"])
##    print("Least anime      : ", min([len(t.loc[user_id]) for user_id in t.index.unique()]))
print_data_count()

def fold_testing(indices):
    print("Separating training and testing data...")
    training_rating_data = rating_data.loc[~rating_data.user_id.isin(indices)]
    testing_rating_data = rating_data.loc[rating_data.user_id.isin(indices)]

    print("Creating training watch data...")
    watch_data = create_watch_data(training_rating_data)

    print("Creating Nearest Neighbors model...")
    distance_model = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    distance_model.fit(watch_data)

    print("Separating test users...")
    test_users = [testing_rating_data.loc[testing_rating_data.user_id == user_id] for user_id in indices]

    print("For each user...")
    accs = []
    pres = []
    recs = []
    for test_user in test_users:
        l = int(len(test_user) / 3)
        print("Fetching target anime...")
        target_anime = test_user.sample(n=l)

        print("Filtering out target anime from history...")
        keys = ["user_id", "anime_id"]
        i1 = test_user.set_index(keys).index
        i2 = target_anime.set_index(keys).index
        data_anime = test_user[~i1.isin(i2)]
        
        print("Fetching predictions...")
        distances, indices = distance_model.kneighbors(watch_data.loc[watch_data.index.isin(data_anime.anime_id.values)], n_neighbors = knn_k + 1)
        indices = indices[:, 1:].flatten()
        ones = [np.any(anime != 1.0) for anime in distances[:, 1:]]
        predicted_anime = set([full_anime_data.iloc[int(i)].MAL_ID for i in indices])
        target_anime = set(target_anime.anime_id.to_list())

        # print("Counting anime in prediction and in target as True Positive...")
        tp = len(predicted_anime.intersection(target_anime))
        # print("Counting anime not in prediction but in target as False Negative...")
        fn = len(target_anime.difference(predicted_anime))
        # print("Counting anime in prediction but not in target as False Positive...")
        fp = len(predicted_anime.difference(target_anime))
        # print("Deducting number of anime user watched minus number of anime targetted as as True Negative...")
        tn = len(data_anime)

        acc = (tp + tn) / (tp + tn + fp + fn)
        pre = (tp) / (tp + fp)
        rec = (tp) / (tp + fn)

        accs.append(acc)
        pres.append(pres)
        recs.append(recs)

        print("TP " + str(tp) + ", FN " + str(fn) + ", FP " + str(fp) + ", TN " + str(tn))
        print("Accuracy  : {:3.2f}%".format(acc*100))
        print("Precision : {:3.2f}%".format(pre*100))
        print("Recall    : {:3.2f}%".format(rec*100))
    print("Average performance:")
    print("Accuracy  : {:3.2f}%".format(np.mean(accs*100)))
    print("Precision : {:3.2f}%".format(np.mean(pres*100)))
    print("Recall    : {:3.2f}%".format(np.mean(recs*100)))
    
    
def create_watch_data(rating_data):
    print("Intializing row and columns...")
    anime_c = CategoricalDtype(sorted(full_anime_data.MAL_ID.unique()))
    user_c = CategoricalDtype(sorted(rating_data.user_id.unique()))
    row = rating_data.anime_id.astype(anime_c).cat.codes
    col = rating_data.user_id.astype(user_c).cat.codes

    print("Creating scipy sparse matrix...")
    watch_data = csr_matrix((rating_data["one"], (row, col)), shape=(anime_c.categories.size, user_c.categories.size))

    print("Converting scipy sparse matrix to pandas sparse DataFrame...")
    watch_data = pd.DataFrame.sparse.from_spmatrix(watch_data, index=anime_c.categories, columns=user_c.categories).fillna(0)

    print("Finished making watch data.")
    return watch_data

print("Initializing K-fold cross validation...")
knn_k = 100
rating_data["one"] = 1
n_user = len(user_data)
indices = np.arange(n_user)
np.random.shuffle(indices)
# 320000 / 60000 = 5 user per iterasi
indices = np.array_split(indices, 60000)
# 3 iterasi
fold_testing(indices[0])
fold_testing(indices[17845])
fold_testing(indices[-1])


##keys = list(target_anime[["user_id", "anime_id"]].values)
##i1 = testing_rating_data.set_index(keys).index
##i2 = target_anime.set_index(keys).index
##testing_rating_data = testing_rating_data[~i1.isin(i2)]





















    
