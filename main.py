###
# Ini adalah bagian inisialisasi dari pembuatan model sistem rekomendasi anime.
# Program digunakan untuk menampilkan rangkuman sederhana tentang kondisi data dan
# membersihkan data untuk membuang poin data yang tidak berguna.
###

# Jangan lupa install package pandas, numpy, matplotlib, seaborn
# Pastikan python dan pip sudah terinstall
# Lalu jalankan module_install.bat

# Initialisasi package
# Database Phase
import pandas as pd
import numpy as np
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


# -- Import data
# Ada 2 data yang berisi rating user di dataset, yaitu rating_complete dan anime_list
# Kami memilih rating_complete karena RC adalah file berisi isi dari AL, namun
# sudah difilter sehingga hanya berisi anime yang sudah selesai ditonton user.
# Data ini lebih baik dari aslinya karena kami ingin merekomendasikan anime yang
# bagus bagi user, sehingga anime yang tidak selesai ditonton tidak dapat menjadi
# indikasi baik terhadap kualitas anime. Selain malah mengindikasi terbalik dari
# keingginan kami, anime yang tidak selesai ditonton juga bisa di drop karena
# user memang sedang menontonnya atau ada kesibukan lain sehingga sedang tidak
# dapat menontonnya, sehingga juga tidak dapat menjadi inverse feature.
def load_anime_data():
    return pd.read_csv("Dataset/anime.csv")
anime_data = load_anime_data()

def load_rating_data():
    return pd.read_csv("Dataset/animelist.csv")
rating_data = load_rating_data()

# Cek apakah data sudah sesuai isi csv
def print_data_count():
    print("Number of anime  : ", len(anime_data))
    ##print("Number of anime  : ", len(anime_data.loc[0:999,:]))
    print("Number of users  : ", len(rating_data.groupby('user_id')))
    print("Number of ratings: ", len(rating_data))
print_data_count()


# -- Print data ke text file untuk analisa
# Difilter karena ada karakter Jepang yang menggunakan menggunakan unicode yang tidak
# disupport oleh .txt. Juga, unicode dapat meningkatkan berat file dengan signifikan.
def create_filter():
    del_chars =  " ".join([chr(i) for i in list(range(32)) + list(range(127, 500000))])
    ##print(del_chars)
    return str.maketrans(del_chars, " " * len(del_chars))
trans = create_filter()

def write_anime_data(trans, name):
    with open(str(name) + r'.txt', 'a') as f:
        df_string = anime_data.apply(lambda y: y.apply(lambda x: str(x).translate(trans))).to_string()
        f.write(df_string)
#write_anime_data(trans, "anime_data")

data_per_file = 1000000
def write_rating_data(trans, name, data_per_file):
    num_before_max = int(math.floor(len(rating_data)/data_per_file)*data_per_file)
    for i in range(0, num_before_max, data_per_file):
        print("Writing file-" + str(int((i/data_per_file) + 1)) + "...")
        with open(str(name) + r'_' + str(int((i/data_per_file) + 1)) + r'.txt', 'a') as f:
            df_string = rating_data.iloc[(i):(i+data_per_file),:].apply(lambda y: y.apply(lambda x: str(x).translate(trans))).to_string()
            f.write(df_string)
    print("Writing last file...")
    with open(str(name) + r'_' + str(int((num_before_max / data_per_file) + 1)) + '.txt', 'a') as f:
        df_string = rating_data.iloc[num_before_max:,:].apply(lambda y: y.apply(lambda x: str(x).translate(trans))).to_string()
        f.write(df_string)
    print("Finished writing all ratings data.")
#write_rating_data(trans, "rating_data", data_per_file)

# anime_data berhasil dicetak, tapi rating_data gagal karena terlalu besar filenya
# Maka rating_data harus dipisah menjadi beberapa bagian.
# Buka anime_data.txt di Notepad++ jika mau cek


# -- Tambah kolom jumlah rating
##anime_data["Score-1"] = pd.to_numeric(anime_data["Score-1"], errors="coerce")
##anime_data["Score-2"] = pd.to_numeric(anime_data["Score-2"], errors="coerce")
##anime_data["Score-3"] = pd.to_numeric(anime_data["Score-3"], errors="coerce")
##anime_data["Score-4"] = pd.to_numeric(anime_data["Score-4"], errors="coerce")
##anime_data["Score-5"] = pd.to_numeric(anime_data["Score-5"], errors="coerce")
##anime_data["Score-6"] = pd.to_numeric(anime_data["Score-6"], errors="coerce")
##anime_data["Score-7"] = pd.to_numeric(anime_data["Score-7"], errors="coerce")
##anime_data["Score-8"] = pd.to_numeric(anime_data["Score-8"], errors="coerce")
##anime_data["Score-9"] = pd.to_numeric(anime_data["Score-9"], errors="coerce")
##anime_data["Score-10"] = pd.to_numeric(anime_data["Score-10"], errors="coerce")
##anime_data["Rating_Count"] = anime_data.loc[:,["Score-1","Score-2","Score-3","Score-4","Score-5","Score-6","Score-7","Score-8","Score-9","Score-10"]].astype(float).sum(axis = 1)
# ternyata anime yang ratingnya dibawah 100 user sudah langsung ditandai "Unknown" skornya

# -- Buang poin-poin data yang buruk

# Drop column rating karena kita tidak melihat rating, hanya user sudah atau belum nonton
# Drop column watched_episodes dengan alasan yang sama
rating_data = rating_data.drop(columns=["rating", "watched_episodes"])

# Filter rating yang bukan Currently Watching (1), Completed (2), atau On Hold (3)
filter_rating = rating_data.loc[rating_data.watching_status >= 4]
print("Success creating filter for " + str(len(filter_rating)) + " ratings.")
print("No Ratings that are not Watching, Completed, or On Hold")
rating_data = rating_data.drop(filter_rating.index)
print("Finished filtering rating data.")
print_data_count()

# Drop column watching_status dengan alasan yang sama karena kita sudah filter
rating_data = rating_data.drop(columns=["watching_status"])

# Filter anime yang tipe medianya tidak diketahui
filter_anime = anime_data.loc[(anime_data.Type == "Unknown")]
print("Success creating filter for " + str(len(filter_anime)) + " anime.")
print("No Unknown Type")
anime_data = anime_data.drop(filter_anime.index)
print("Finished filtering anime data.")
print_data_count()

# Filter anime yang skornya tidak diketahui
filter_anime = anime_data.loc[(anime_data.Score == "Unknown")]
print("Success creating filter for " + str(len(filter_anime)) + " anime.")
print("No Unknown Scores")
anime_data = anime_data.drop(filter_anime.index)
print("Finished filtering anime data.")
print_data_count()

# Filter anime yang skornya dirating kurang dari 100 orang
# Ini redundan karena anime dibawah 100 rating sudah memiliki score Unknown dan sudah difilter
##filter_anime = anime_data.loc[(anime_data.Rating_Count < 100)]
##print("Success creating filter for " + str(len(filter_anime)) + " anime.")
##print("No Rating Count less than 100")
##anime_data = anime_data.drop(filter_anime.index)
##print("Finished filtering anime data.")
##print_data_count()

# Filter anime yang tidak PG-18
filter_anime = anime_data.loc[(anime_data.Genres.str.contains("Hentai"))]
print("Success creating filter for " + str(len(filter_anime)) + " anime.")
print("No Hentai")
anime_data = anime_data.drop(filter_anime.index)
print("Finished filtering anime data.")
print_data_count()
                              
# anime_data.to_csv(index=False, path_or_buf='filtered_anime_data.csv')

# Filter juga anime yang didrop pada list rating
filter_rating = rating_data[rating_data.anime_id.isin(filter_anime.MAL_ID.to_list())]
print("Success creating filter for " + str(len(filter_rating)) + " ratings.")
print("No Ratings from Filtered Anime")
rating_data = rating_data.drop(filter_rating.index)
print("Finished filtering rating data.")
print_data_count()

# Tampilkan jumlah rating untuk tiap user
print("Finished calculating user rating count.")
rating_count = rating_data.user_id.value_counts()

# Orang yang menonton lebih dari 10000 sulit dijadikan referensi karena dia kemungkinan hanya menonton
# semua anime yang ada. Opsi lain adalah 5000. 1000 itu "normal" bagi beberapa orang.
greater_than = 10000
filter_rating = rating_data[rating_data.user_id.isin(rating_count.index[rating_count.gt(10000)])]
print("Success creating filter for " + str(len(filter_rating)) + " ratings.")
print("No Ratings from Users with more than 10000 anime rated")
rating_data = rating_data.drop(filter_rating.index)
print("Finished filtering rating data.")
print_data_count()

# Orang yang menonton kurang dari 10 sulit dijadikan referensi karena kemungkinan besar dia bukan
# penggemar besar, atau mungkin tidak menginput datanya dengan penuh. Opsi lain 20/50.
lesser_than = 10
filter_rating = rating_data[rating_data.user_id.isin(rating_count.index[rating_count.lt(10)])]
print("Success creating filter for " + str(len(filter_rating)) + " ratings.")
print("No Ratings from Users with less than 10 anime rated")
rating_data = rating_data.drop(filter_rating.index)
print("Finished filtering rating data.")
print_data_count()

rating_data.to_csv(index=False, path_or_buf='filtered_rating_data.csv')

##write_anime_data(trans, "filtered_anime_data")
##write_rating_data(trans, "filtered_rating_data", data_per_file)

