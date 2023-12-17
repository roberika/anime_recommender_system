###
# Ini adalah bagian utama dari pembuatan model sistem rekomendasi anime.
# Program ini akan melatih, menampilkan hasil evaluasi model, dan menyimpan model.
###

# Jangan lupa install package pandas, numpy, matplotlib, seaborn
# Pastikan python dan pip sudah terinstall
# Lalu jalankan module_install.bat

# Initialisasi package
import pandas as pd
import pickle
import numpy as np
from scipy.sparse import csr_matrix
from pandas.api.types import CategoricalDtype
import sklearn
from sklearn.neighbors import NearestNeighbors
import math
pd.set_option('display.max_columns', 500)

# -- Initialisasi array user-anime
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

# Membuat kolom anime dan baris user
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
k = 50

def get_random_anime():
    return np.random.choice(watch_data.shape[0])
    print("Anime ID :", random_index)
    print("Anime Name :", get_anime_by_id(random_index))

def generate_recommendation(index, k): # There's your hint Robert. This and flatten. You're almost there.
    return distance_model.kneighbors(np.reshape(watch_data.iloc[index, :].values,(1,-1)), n_neighbors = k + 1)

def generate_recommendations(anime_watch_data, k): # Yeaahhh this works, baebey!
    return distance_model.kneighbors(anime_watch_data, n_neighbors = k + 1)

def print_recommendation(anime_id, distances, indices):
    print('Recommendations for {0}:\n'.format(get_anime_by_id(anime_id)))
    for i in range(0, len(distances)):
        print('{0}: {1}, with distance of {2}:'.format(i, get_name_by_id(get_id_by_index(indices[i])), distances[i]))
        
def get_name_by_id(id):
    return full_anime_data.loc[full_anime_data.MAL_ID==id].Name.values[0]

def get_name_by_index(index):
    return full_anime_data.iloc[index].Name

def get_index_by_id(id):
    return full_anime_data.loc[full_anime_data.MAL_ID == id].index.values[0]

def get_id_by_index(index):
    return full_anime_data.iloc[index].MAL_ID

def get_anime_by_index(index):
    return full_anime_data.iloc[index]

def get_recommendation(anime_id, k):
    index = get_index_by_id(anime_id)
    distances, indices = generate_recommendation(index, k)
    print_recommendation(anime_id, distances.flatten(), indices.flatten())

def get_random_recommendation():
    random_id = get_random_anime()
    get_recommendation(random_id)

def create_anime_recommendation_model(k):
    # Tentukan anime yang bertetangga dekat
    print("Rendering "+str(k)+" nearest neighbors for each anime...")
    distances, indices = generate_recommendations(watch_data, k)
    indices = indices[:, 1:]

    # Filter anime yang hanya punya distance 1.0
    # Anime seperti itu tidak memiliki anime tetangga,
    # sehingga tidak dapat dibilang data yang bagus
    ones = [np.any(anime != 1.0) for anime in distances[:, 1:]]

    # Ubah data index jadi data ID anime
    print("Replacing indices with IDS...")
    indices = np.array([[get_id_by_index(int(j)) for j in i] for i in indices])

    # Simpan anime ke dalam DataFrame
    print("Creating DataFrame...")
    rendered_distance_model = pd.DataFrame(indices, columns = [*range(1, k+1)])
    rendered_distance_model["MAL_ID"] = full_anime_data["MAL_ID"]
    rendered_distance_model = rendered_distance_model.loc[ones]
    return rendered_distance_model

def save_anime_recommendation_model():
    print("Saving recommendation model...")
    pickle.dump(rendered_distance_model, open('anime_recommendation_model.sav', 'wb'))

#rendered_distance_model = create_anime_recommendation_model(100)
#save_anime_recommendation_model()

def print_connection():
    k = 10
    print("Rendering distances " + str(k) + " nearest neighbor for each anime...")
    distances, indices = generate_recommendations(watch_data[0:100], k)
    heads = indices[:, 0].flatten()
    indices = indices[:, 1:]
    distances = distances[:, 1:]

    print("Create filter...")
    ones = [np.any(anime != 1.0) for anime in distances]
    heads = heads[ones]
    indices = indices[ones]
    distances = distances[ones]

    print("Fetching names and making lists...")
    names = np.array([
        [get_name_by_index(int(rec)) for rec in np.repeat(heads, k).flatten()],
        [get_name_by_index(int(rec)) for rec in indices.flatten()],
        distances.flatten()
             ])

    print("Creating DataFrame...")
    links = pd.DataFrame(data={'from': names[0], 'to': names[1], 'distance': names[2]})
    points = pd.DataFrame([get_name_by_index(int(rec)) for rec in heads.flatten()], columns=["anime"])

    print("Save it...")
    links.to_csv(index=False, path_or_buf='links.csv')
    points.to_csv(index=False, path_or_buf='points.csv')

    print("Distance model rendered.")
#print_connection()

def print_user_data(user_id):
    user = rating_data.loc[(rating_data.user_id == user_id) & (rating_data.rating != 0)].copy()
    user = user.drop(columns=["one", "user_id"])
    user = append_anime_name(user)
    print(user)

def append_anime_name(rating_data):
    return pd.merge(rating_data, full_anime_data[['Name', 'MAL_ID']], how='left', left_on='anime_id', right_on='MAL_ID').drop(columns=["MAL_ID"])

def indices_to_ids(indices):
    indices = pd.DataFrame(indices.flatten().tolist()).rename(columns={0: 'index'})
    full_anime_data["index"] = full_anime_data.index
    indices = pd.merge(indices, full_anime_data[['index', 'MAL_ID']], how='left', left_on='index', right_on='index')
    return indices

def guess_score(user_id, anime_id):
    user = rating_data.loc[(rating_data.user_id == user_id) & (rating_data.rating != 0)].copy()
    user = user.drop(columns=["one", "user_id"])
    user_item = user.loc[user.anime_id == anime_id]
    if len(user_item) == 0:
        print("User didn't watch this anime")
        return
    print(full_anime_data.loc[full_anime_data.MAL_ID == anime_id].Name.values[0])
    target_score = user_item.rating.values[0]
    user = user.drop(user_item.index)
    distances, indices = generate_recommendation(get_index_by_id(anime_id), k)
    indices = indices_to_ids(indices)['MAL_ID']
    nearest_anime = user.loc[user.anime_id.isin(indices)]
    if len(nearest_anime) > 0:
        predicted_score = nearest_anime.rating.mean()
        print("Nearest anime   :\n", append_anime_name(nearest_anime))
        print("Target Score    :", target_score)
        print("Predicted Score :", predicted_score)
        print("Rounded PS      :", int(predicted_score))
    else:
        print("User didn't watch similiar anime")

def simulation():
    while(True):
        print("Anime Score Predictor")
        user_id = input("Select a user ID: ")
        if user_id == "Q": break
        print("This user watches:")
        print_user_data(int(user_id))
        while(True):
            anime_id = input("Select an anime ID: ")
            if anime_id == "Q": break
            guess_score(int(user_id), int(anime_id))



# 400 MB files nopers
##def create_anime_recommendation_model(k):
##    # Hitung jarak antar anime
##    print("Rendering distances " + str(k) + " nearest neighbor for each anime...")
##    distances, indices = generate_recommendations(watch_data, k)
##    distances = distances[:, 1:]
##    indices = indices[:, 1:]
##
##    # Filter anime yang hanya punya distance 1.0
##    # Anime seperti itu tidak memiliki anime tetangga,
##    # sehingga tidak dapat dibilang data yang bagus
##    print("Create filter...")
##    ones = [np.any(anime != 1.0) for anime in distances]
##
##    # Ubah data index jadi data ID anime dan nama anime 
##    print("Fetch IDs and names...")
##    names = [[get_name_by_index(int(j)) for j in i] for i in indices]
##    indices = [[get_id_by_index(int(j)) for j in i] for i in indices]
##
##    # Gabungkan jadi 1 array
##    print("Combine to one array...")
##    rendered_data = np.append(indices, names, axis = 1)
##
##    # Simpan jarak ke dalam DataFrame
##    print("Creating DataFrame...")
##    cols = [("-" + str(i) + "-" + str(j)) for j in ["i", "n"] for i in range(1, k+1)]
##    rendered_distance_model = pd.DataFrame(rendered_data, columns = cols)
##    rendered_distance_model['MAL_ID'] = full_anime_data.MAL_ID
##    rendered_distance_model.set_index('MAL_ID')
##    rendered_distance_model = rendered_distance_model.loc[ones]
##
##    # Gabungkan jarak dan index anime
##    print("Combine columns...")
##    for i in range(1,k+1):
##        j = str(i)
##        combine = [col for col in rendered_distance_model.columns if str("-" + j + "-") in col]
##        rendered_distance_model[j] = rendered_distance_model.apply(lambda r: tuple(r.loc[combine]), axis=1).apply(np.array)
##    rendered_distance_model = rendered_distance_model.drop(columns = cols)
##
##    print("Distance model rendered.")
##    return rendered_distance_model
##
##def save_anime_recommendation_model():
##    print("Saving recommendation model...")
##    pickle.dump(rendered_distance_model, open('anime_recommendation_model.sav', 'wb'))
##
##rendered_distance_model = create_anime_recommendation_model(100)
##save_anime_recommendation_model()

##def create_anime_recommendation_model(k):
##    # Hitung jarak antar anime
##    print("Rendering distances 20 nearest neighbor for each anime...")
##    distances, indices = generate_recommendations(watch_data, k)
##    distances = distances[:, 1:]
##    indices = indices[:, 1:]
##
##    # Ubah data index jadi data ID anime
##    indices = [[get_id_by_index(int(j)) for j in i] for i in indices]
##
##    # Gabungkan jadi 1 array
##    print("Combine to one array...")
##    rendered_data = np.append(indices, distances, axis = 1)
##
##    # Simpan jarak ke dalam DataFrame
##    print("Creating DataFrame...")
##    cols = [("-" + str(i) + "-" + str(j)) for j in ["i", "d"] for i in range(1, k+1)]
##    rendered_distance_model = pd.DataFrame(rendered_data, columns = cols)
##    rendered_distance_model['MAL_ID'] = full_anime_data.MAL_ID
##    rendered_distance_model.set_index('MAL_ID')
##
##    # Gabungkan jarak dan index anime
##    print("Combine columns...")
##    for i in range(1,k+1):
##        j = str(i)
##        combine = [col for col in rendered_distance_model.columns if str("-" + j + "-") in col]
##        rendered_distance_model[j] = rendered_distance_model.apply(lambda r: tuple(r.loc[combine]), axis=1).apply(np.array)
##    rendered_distance_model = rendered_distance_model.drop(columns = cols)
##    return rendered_distance_model

##def save_anime_rating_model():
##    print("Saving recommendation model...")
##    pickle.dump(distance_model, open('anime_rating_model.sav', 'wb'))
# Terlalu berat
##save_anime_rating_model()

# def get_recommendation_for_user(user_id):
    # watch_list = rating_data.loc[rating_data.user_id == user_id].anime_id
    # recommendation_list = pd.Series([])
    # for anime_id in watch_list:
        # index = full_anime_data.loc[full_anime_data.MAL_ID == anime_id].index.values[0]
        # distances, indices = generate_recommendation(index, k)
        # recommendation_list = recommendation_list._append(pd.Series(distances.flatten(), index=indices.flatten()))
    # print_recommendation_for_user(user_id, recommendation_list)

##def print_recommendation_for_user(user_id, recommendation_list):
##    distances = recommendation_list.values
##    indices = recommendation_list.index
##    print('Recommendations for user of ID {0}:\n'.format(user_id))
##    for i in range(0, len(distances)):
##        print('{0}: {1}, with distance of {2}:'.format(i, get_anime_by_id(watch_data.index[indices[i]]), distances[i]))


##def save_model():
##    distances, indices = generate_recommendations(watch_data, 17562)
##    full_anime_data["Recommendation ID"] = indices[:, 1:]
##    full_anime_data["Recommendation Distances"] = distances[:, 1:]
##    pickle.dump(full_anime_data, open('anime_data.sav', 'wb'))
##print("Saving model...")
##save_model()

# Ubah jarak jadi matrix segitiga atas tanpa diagonal
# Ini menghemat memori karena jarak antara sebuah anime dengan dirinya
# sendiri pasti 0, dan jarak antara 2 anime yang sebelumnya ditulis
# 2 kali sekarang hanya ditulis 1 kali.
##size = len(full_anime_data)
##triangular_data = np.zeros((size, size))
##triangular_data[np.triu_indices(size, 1)] = distances

# Menyimpan model kedalam disk
# pickle.dump(distance_model, open('model.sav', 'wb'))

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

##with open(r'model.dart', 'a') as f:
##    f.write("class Model {")
##    f.write("var animeList = [\n")
##    f.close()

# Membuat class Dart berisi data anime
# Supaya Panda tidak menambah ... di akhir kolom
##def create_anime_class():
##    pd.set_option("display.max_colwidth", None)
##    print("Drop everything else to save memory")
##    full_anime_data = full_anime_data.drop(columns=["English name", "Japanese name", "Episodes", "Aired", "Producers", "Licensors", "Duration", "Rating", "Ranked", "Popularity", "Members", "Favorites", "Completed", "On-Hold", "Dropped", "Plan to Watch", "Score-10", "Score-9", "Score-8", "Score-7", "Score-6", "Score-5", "Score-4", "Score-3", "Score-2", "Score-1"])
##    print("Writing dart class...")
##    full_anime_data["Dart"] = 'Anime(\nid: ' + full_anime_data["MAL_ID"].astype(str) + ',\nname: "' + full_anime_data["Name"].astype(str) + '",\nscore: ' + full_anime_data["Score"].astype(str) + ',\ngenres: "' + full_anime_data["Genres"].astype(str) + '",\ntype: "' + full_anime_data["Type"].astype(str) + '",\npremiered: "' + full_anime_data["Premiered"].astype(str) + '",\nstudios: "' + full_anime_data["Studios"].astype(str) + '",\n),'
##    with open(r'anime_data.dart', 'a', encoding="utf-8") as f:
##        f.write("class Model {\nvar animeList = [\n" + full_anime_data[["Dart"]].to_string(header=False, justify="left", index=False) + "\n];\n}\n")
##        f.close()

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

























