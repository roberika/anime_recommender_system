import pickle
import requests as rq
import numpy as np
import pandas as pd
import sklearn

# Muat model jarak KNN antar anime yang sudah di hitung sebelumnya
def load_model():
    global anime_recommendation_model
    anime_recommendation_model = pickle.load(open('dataset/anime_recommendation_model.sav', 'rb'))

# Muat list anime yang user sudah tonton beserta skornya
# user_history berisi semua anime, digunakan untuk rekomendasi
# user_scores berisi anime yang memiliki skor bukan 0 (belum dinilai),
# digunakan untuk prediksi skor
# Difilter supaya tidak memuat ID diatas 48492 karena dataset hanya
# memiliki anime sampai ID tersebut
def load_user_list(username):
    global user_history
    global user_scores
    item_per_page = 1000
    i = 1
    url = "https://api.myanimelist.net/v2/users/"+str(username)+"/animelist?fields=node,list_status&limit=" + str(item_per_page)
    headers = {'X-MAL-CLIENT-ID': 'fe954b2111fb0add5b5b25bfaa638979', 'Accept': '*/*'}
    response = rq.get(url, headers=headers)
    user = response.json()["data"]
    while (len(response.json()["paging"]) != 0 and len(response.json()["paging"]["next"]) != 0):
        response = rq.get(url + "&offset=" + str(item_per_page * i), headers=headers)
        user = user | response.json()["data"]
        i += 1
    #user = [anime["node"] | anime["list_status"]  for anime in user]
    #user = {anime["id"]: {key: value for key, value in anime.items() if key != 'id'} for anime in user}
    #user_history = {anime["node"]["id"]: anime["list_status"]["score"] for anime in user}
    ids = [anime["node"]["id"] for anime in user]
    scores = [anime["list_status"]["score"] for anime in user]
    list_anime = {"anime_id": ids, "rating": scores}
    user_history = pd.DataFrame({"anime_id": ids, "rating": scores})
    user_history = user_history.loc[user_history.anime_id <= 48492]
    user_scores = user_history.loc[user_history.rating != 0]
##    print(user_history)
##    print(user_scores)

def get_name_by_id(data, id):
    return data.loc[data.MAL_ID==id].Name.values[0]

def get_recommendation(anime_id):
    return anime_recommendation_model.loc[anime_recommendation_model.MAL_ID == anime_id].values.flatten()[:-1]

def get_recommendations(anime_ids):
    recs = anime_recommendation_model.loc[anime_recommendation_model.MAL_ID.isin(anime_ids)].values.flatten()
    recs = [i for i in recs if i not in anime_ids]
    recs_sorted, indices = np.unique(np.array(recs), return_index=True)
    return [recs[index] for index in sorted(indices)]

def append_predicted_scores(anime_list):
    return [[rec, user_scores.loc[user_scores.anime_id.isin(get_recommendation(rec))].rating.mean()] for rec in anime_list]

def get_recommendation_with_scores(anime_id):
    return append_predicted_scores(get_recommendation(anime_id))

def get_recommendations_with_scores(anime_ids):
    return append_predicted_scores(get_recommendations(anime_ids))

def get_recommendations(anime_ids):
    recs = anime_recommendation_model.loc[anime_recommendation_model.MAL_ID.isin(anime_ids)].values.flatten()
    recs = [i for i in recs if i not in anime_ids]
    recs_sorted, indices = np.unique(np.array(recs), return_index=True)
    return [recs[index] for index in sorted(indices)]

def get_recommendations_for_current_user():
    return get_recommendations(user_history.anime_id.to_list())

def get_recommendations_for_current_user_with_scores():
    return get_recommendations_with_scores(user_history.anime_id.to_list())

def print_recommendations(data, recs, limit):
    for i, rec in enumerate(recs[:limit]):
        print('{:5.0f}: '.format(i + 1) + get_name_by_id(data, rec))

def print_recommendations_with_scores(data, recs_with_scores, limit):
    for i, rec in enumerate(recs_with_scores[:limit]):
        if(np.isnan(rec[1])):
            print('{:5.0f}: '.format(i + 1) + get_name_by_id(data, rec[0]) + " [-]")
        else:
            print('{:5.0f}: '.format(i + 1) + get_name_by_id(data, rec[0]) + " [{:2.2f}]".format(rec[1]))
        
def load_anime_data():
    return pd.read_csv("dataset/anime.csv")

def demonstration():
    amount = 20
    recs = []
    option = ''
    
    print("RKMDaa - Anime Recommendation System")
    full_anime_data = load_anime_data()
    load_model()
    print("Welcome! ^^")
    username = input("Please input your MAL username! ")
    load_user_list(username)
    print("Creating recommendations for you...")
    recs = get_recommendations_for_current_user_with_scores()
    while(option.upper() != 'N'):
        print("Here's what I can do, " + username + "-sama")
        print(" [H] Recommend anime from what you've watched")
        print(" [A] Recommend anime from another anime")
        print(" [P] Predict an anime's score")
        print(" [S] Set number of anime recommended")
        option = input("What do you want to do UwU : ")
        if(option.upper() == 'H'):
            print("Here's the " + str(amount) + " anime we'd recommend for you, master!")
            print_recommendations_with_scores(full_anime_data, recs, amount)
        elif(option.upper() == 'A'):
            option = int(input("Can you give me the anime ID, kudasai? ").strip())
            print("[" + get_name_by_id(full_anime_data, option) + "], is it? Well, here you go!")
            print_recommendations_with_scores(full_anime_data, get_recommendation_with_scores(option), amount)
        elif(option.upper() == 'P'):
            option = int(input("Can you give me the anime ID, kudasai? ").strip())
            nearest_anime = user_scores.loc[user_scores.anime_id.isin(get_recommendation(option))]
            if(len(nearest_anime) == 0):
                print("I'm sorry, teacher, but I can't give an accurate estimate for [" + get_name_by_id(full_anime_data, option) + "].")
                print("You haven't watched enough anime similiar to it. -~-\"")
            else:
                predicted_rating = nearest_anime.rating.mean()
                print("I think you'll give [" + get_name_by_id(full_anime_data, option) + "] a " + '{:.2f}'.format(predicted_rating))
                print("We estimated it from these anime:")
                print_recommendations(full_anime_data, nearest_anime.anime_id.values, amount)
        else:
            option = input("What do you want to set it to? ")
            amount = int(option)
            print("I've set the amount to " + option + ". Your welcome!")
        option = input("Anything else, commander? ")
    print("See you later doctor!")
        











## Testing
##load_model()
##print(anime_recommendation_model)
##load_user_list("WWWalter")
##anime_id = 1
##anime_ids = [1, 5, 6]
##rec = get_recommendation(anime_id)
##recs = get_recommendations(anime_ids)
##recs = get_recommendations_for_current_user()
##print_recommendations(recs, 100)
##print(rec, len(rec))
##print(recs, len(recs))
    
