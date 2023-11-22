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
    return pd.read_csv("Dataset/anime.csv")
full_anime_data = load_anime_data()
print(full_anime_data.shape)

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
# Untuk categorinya pakai full_anime_data karena ada beberapa anime yang
# tidak ada di anime_data karena berasal dari rating_data yang difilter.
print("Intializing anime categorical D type...")
anime_c = CategoricalDtype(sorted(full_anime_data.MAL_ID.unique()))

print("Intializing user categorical D type...")
user_c = CategoricalDtype(sorted(rating_data.user_id.unique()))

print("Intializing anime row...")
row = rating_data.anime_id.astype(anime_c).cat.codes

print("Intializing user col...")
col = rating_data.user_id.astype(user_c).cat.codes

# Tambah kolom berisi satu supaya jadi isi sparse matrix
rating_data["one"] = 1

print("Creating scipy sparse matrix...")
watch_data = csr_matrix((rating_data["one"], (row, col)), shape=(anime_c.categories.size, user_c.categories.size))

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
print("Creating Nearest Neighbors model...")
distance_model = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
distance_model.fit(watch_data)

# Mengambil anime id random, lalu generate k neighbors sebagai anime yang
# audiencenya paling dekat dengan anime tersebut. Diberi
# watch_data.iloc[random_index, :].value.reshape(1, -1) karena kita mau
# memasukkan hanya anime baru tersebut dan sparse matrix penonton anime
# baru itu sebagai input. K + 1 karena anime pertama yang ditampilkan,
# anime terdekat dengan anime input, ialah anime itu sendiri yang ada di
# dalam modelnya.
k = 10

def get_anime_by_id(id):
    return full_anime_data.loc[full_anime_data.MAL_ID==id].Name.values

def get_random_anime():
    return np.random.choice(watch_data.shape[0])
    print("Anime ID :", random_index)
    print("Anime Name :", get_anime_by_id(random_index))

def generate_recommendation(indices, k): # There's your hint Robert. This and flatten. You're almost there.
    return distance_model.kneighbors(np.reshape(watch_data.iloc[indices, :].values,(1,-1)), n_neighbors = k + 1)

def print_recommendation(anime_id, distances, indices):
    print('Recommendations for {0}:\n'.format(get_anime_by_id(anime_id)))
    for i in range(0, len(distances)):
        print('{0}: {1}, with distance of {2}:'.format(i, get_anime_by_id(watch_data.index[indices[i]]), distances[i]))

def get_recommendation(anime_id):
    index = full_anime_data.loc[full_anime_data.MAL_ID == anime_id].index.values[0]
    distances, indices = generate_recommendation(index, k)
    print_recommendation(anime_id, distances.flatten(), indices.flatten())

def get_random_recommendation():
    random_id = get_random_anime()
    get_recommendation(random_id)
#get_random_recommendation()

def get_recommendation_for_user(user_id):
    watch_list = rating_data.loc[rating_data.user_id == user_id].anime_id
    recommendation_list = pd.Series([])
    for anime_id in watch_list:
        index = full_anime_data.loc[full_anime_data.MAL_ID == anime_id].index.values[0]
        distances, indices = generate_recommendation(index, k)
        recommendation_list = recommendation_list._append(pd.Series(distances.flatten(), index=indices.flatten()))
    print_recommendation_for_user(user_id, recommendation_list)
    
def print_recommendation_for_user(user_id, recommendation_list):
    distances = recommendation_list.values
    indices = recommendation_list.index
    print('Recommendations for user of ID {0}:\n'.format(user_id))
    for i in range(0, len(distances)):
        print('{0}: {1}, with distance of {2}:'.format(i, get_anime_by_id(watch_data.index[indices[i]]), distances[i]))

##with open(r'model.dart', 'a') as f:
##    f.write("class Model {")
##    f.write("var animeList = [\n")
##    f.close()

# Membuat class Dart berisi data anime
# Supaya Panda tidak menambah ... di akhir kolom
pd.set_option("display.max_colwidth", None)
print("Drop everything else to save memory")
full_anime_data = full_anime_data.drop(columns=["English name", "Japanese name", "Episodes", "Aired", "Producers", "Licensors", "Duration", "Rating", "Ranked", "Popularity", "Members", "Favorites", "Completed", "On-Hold", "Dropped", "Plan to Watch", "Score-10", "Score-9", "Score-8", "Score-7", "Score-6", "Score-5", "Score-4", "Score-3", "Score-2", "Score-1"])
print("Writing dart class...")
full_anime_data["Dart"] = 'Anime(\nid: ' + full_anime_data["MAL_ID"].astype(str) + ',\nname: "' + full_anime_data["Name"].astype(str) + '",\nscore: ' + full_anime_data["Score"].astype(str) + ',\ngenres: "' + full_anime_data["Genres"].astype(str) + '",\ntype: "' + full_anime_data["Type"].astype(str) + '",\npremiered: "' + full_anime_data["Premiered"].astype(str) + '",\nstudios: "' + full_anime_data["Studios"].astype(str) + '",\n),'
with open(r'anime_data.dart', 'a', encoding="utf-8") as f:
    f.write("class Model {\nvar animeList = [\n" + full_anime_data[["Dart"]].to_string(header=False, justify="left", index=False) + "\n];\n}\n")
    f.close()

# Ini membuat class Dart untuk menyimpan data anime bersama rekomendasinya. Tidak dipakai karena terlalu lamban
##k = 100
##with open(r'anime_data.dart', 'a') as f:
##    f.write("class Model {\nvar animeList = [\n")
##    for part in range(0,176):
##        end = ((part+1)*100)
##        if part == 175:
##            end = 17562
##        s = ''
##        for i in range((part*100),end):
##            anime = full_anime_data.iloc[i]
##            s += 'Anime(\nid: ' + str(anime.MAL_ID) + ',\nname: "' + str(anime.Name) + '",\nscore: ' + str(anime.Score) + ',\ngenres: ' + str(anime.Genres.split(", ")) + ',\ntype: "' + str(anime.Type) + '",\npremiered: "' + str(anime.Premiered) + '",\nstudios:' + str(anime.Studios.split(", ")) + ',\nrecommendations: [\n'
##            distances, indices = generate_recommendation(i, k)
##            distances = distances.flatten()[1:]
##            indices = indices.flatten()[1:]
##            for r in range(0, k):
##                s += 'Distance(id: ' + str(full_anime_data.iloc[indices[r]].MAL_ID) + ', distance: ' + str(int(distances[r] * 10000)) + '),\n'
##            s += '],\n),\n'
##            print("Finished writing " + str(anime.MAL_ID) + "(" + str(i) + ")")
##        f.write(s)
##        print("Milestone " + str(part) + " x 100")
##    f.write("];\n}\n")
##    f.close()
    
##with open(r'model.dart', 'a') as f:
##    f.write("];\n}\n")
##    f.close()



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

























