###
# Ini adalah bagian utama dari pembuatan model sistem rekomendasi anime.
# Program ini akan melatih, menampilkan hasil evaluasi model, dan menyimpan model.
###

# Jangan lupa install package pandas, numpy, matplotlib, seaborn
# Pastikan python dan pip sudah terinstall
# Lalu jalankan module_install.bat

# Initialisasi package
# Database Phase
import pandas as pd
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


# -- Initialisasi array user-anime
def load_anime_data():
    return pd.read_csv("filtered_anime_data.csv")
full_anime = load_anime_data()
print(full_anime.shape)

def load_rating_data():
    return pd.read_csv("filtered_rating_data.csv")
rating_data = load_rating_data()
print(rating_data.shape)

def get_anime(rating_data):
    return rating_data.anime_id.drop_duplicates()
anime_data = get_anime(rating_data)

def get_users(rating_data):
    return rating_data.user_id.drop_duplicates()
user_data = get_users(rating_data)

# Cek apakah data sudah sesuai isi csv
def print_data_count():
    print("Number of anime  : ", len(anime_data))
    ##print("Number of anime  : ", len(anime_data.loc[0:999,:]))
    print("Number of users  : ", rating_data['user_id'].max())
    print("Number of ratings: ", len(rating_data))
print_data_count()

# -- Membuat sparse matrix berisi anime yang sudah ditonton tiap user
print("Intializing anime categorical D type...")
anime_c = CategoricalDtype(sorted(rating_data.anime_id.unique()))

print("Intializing user categorical D type...")
user_c = CategoricalDtype(sorted(rating_data.user_id.unique()))

print("Intializing anime row...")
row = rating_data.anime_id.astype(anime_c).cat.codes

print("Intializing user col...")
col = rating_data.user_id.astype(user_c).cat.codes

print("Creating scipy sparse matrix...")
watch_data = csr_matrix((rating_data["rating"]/rating_data["rating"], (row, col)), shape=(anime_c.categories.size, user_c.categories.size))

# Harus diubah karena ada beberapa fungsi yang saya temukan yang lebih mudah
# dipakai jika dalam bentuk Data Frame
print("Converting scipy sparse matrix to pandas sparse DataFrame...")
watch_data = pd.DataFrame.sparse.from_spmatrix(watch_data, index=anime_c.categories, columns=user_c.categories).fillna(0)

# Note: this is copied. Please check the docs to actually understand the code.
# I'm too tired to do it now.
# NearestNeighbors adalah algoritma untuk secara otomatis menghitung jarak
# antara dua objek dari library sklearn. Metric yang digunakan di set pada
# cosine similiarity karena kita mau melihat apakah anime A ditonton oleh
# audience yang sama dengan anime B. Algorithm yang tersedia adalah brute, K-Tree,
# dan Ball Tree, tetapi yang kita pakai adalah brute sesuai rekomendasi dari
# sklearn untuk menggunakan brute jika input datanya berbentuk sparse matrix,
# metricnya precomputed atau sudah ada, dimensi jarak lebih dari 15, jumlah k
# lebih dari atau sama dengan setengah dari jumlah data, dan effective metric
# tidak dalam valid metric.
# Untuk kasus kita, kita memenuhi kondisi 1 dan 3 karena input data kita memang sparse
# dan dimensi kita sesuai dengan jumlah user dan sudah pasti lebih dari 15.
distance_model = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
distance_model.fit(watch_data)

# Mengambil anime id random, lalu generate k neighbors sebagai anime yang
# audiencenya paling dekat dengan anime tersebut. Diberi
# watch_data.iloc[random_index, :].value.reshape(1, -1) karena kita mau
# memasukkan hanya anime baru tersebut dan sparse matrix penonton anime
# baru itu sebagai input. K + 1 karena anime pertama yang ditampilkan,
# anime terdekat dengan anime input, ialah anime itu sendiri yang ada di
# dalam modelnya.
k = 5

def get_anime_by_id(id):
    return full_anime.loc[full_anime.MAL_ID==id].Name.values

def get_random_anime():
    return np.random.choice(watch_data.shape[0])
    print("Anime ID :", random_index)
    print("Anime Name :", get_anime_by_id(random_index))
random_index = get_random_anime()

def generate_recommendation():
    return distance_model.kneighbors(np.reshape(watch_data.iloc[random_index, :].values,(1,-1)), n_neighbors = k + 1)
distances, indices = generate_recommendation()

def print_recommendation(distances, indices):
    for i in range(0, len(distances.flatten())):
        if i == 0:
            print('Recommendations for {0}:\n'.format(get_anime_by_id(watch_data.index[random_index])))
        else:
            print('{0}: {1}, with distance of {2}:'.format(i, get_anime_by_id(watch_data.index[indices.flatten()[i]]), distances.flatten()[i]))
print_recommendation(distances, indices)




# Tidak bisa disave jadi csv karena terlalu besar, jadi kode diatas harus terus dijalankan saja
# ----
# Tidak bisa dijalankan secara sekaligus, saya sudah coba dan semalaman masih belum
# selesai. Jadi, saya pisah dulu jadi 4 bagian .csv, lalu baru digabung.
##split = 4
##length_per_split = int(math.floor(len(watch_data)/(split-1)))
##for i in range(0,split-1):
##    print("Writing file ", i+1)
##    watch_data.iloc[(i*length_per_split) : ((i+1)*length_per_split),:].to_csv(index=False, path_or_buf=("watch_data_" + str(i+1) + ".csv"))
##print("Writing last file")
##watch_data.iloc[((split-1)*length_per_split):,:].to_csv(index=False, path_or_buf=("watch_data_" + str(split) + ".csv"))

# Ini cara official DULU. Sekarang dtw ngapo dk biso untuk buat sparse matrix.
##print("Start conversion...")
##watch_data = rating_data.pivot_table(values="rating", index='anime_id', columns='user_id', aggfunc="count", fill_value=0)
##print(watch_data.head())

# Cara ini bisa juga dan lebih cepat dari cara dibawah, tapi masih sangat memakan
# waktu dan bukan cara yang lazim dipakai oleh developer lain. Selanjutnya,
# saya coba pakai pivot_table().
##uwa = pd.DataFrame({'anime_id': anime_data})
##uwa.set_index("anime_id")
##print(uwa.head)
##for users in user_data:
##    uwa[users] = 0
##    for anime in rating_data.loc[(rating_data.user_id == users)].anime_id:
##        uwa.loc[anime, users] = 1
##    print("Finished adding user " + str(users) + "'s watchlist.")
##print(uwa.head)

# Cara ini bisa, berhasil, tapi sangat lama dan tidak efisien
# Ini O(m*n), m jumlah anime, n jumlah user
# Yang diatas O(m*n), m jumlah anime yang dinonton user X, n jumlah user
### user-watched-anime matrix, 1 kalau user sudah nonton, 0 kalau belum.
### also, uwa karena belajar panda rasony cak belajar bahaso program bru karena
### beda nian dari basic py.
##uwa = pd.DataFrame({'anime_id': anime_data})
##print(uwa)
##for users in user_data:
###for users in range(500, 510):
##    #print(len(rating_data.loc[(rating_data.user_id == users)]))
##    anime_user_watched = rating_data.loc[(rating_data.user_id == users)]
##    to_add = [(1 if (anime_user_watched.anime_id.astype(str).str.contains(str(anime)).any()) else 0) for anime in anime_data]
##    uwa[str(users)] = np.asarray(to_add)
##    print("Finished adding user " + str(users) + "'s watchlist.")
###print(uwa.head)

























