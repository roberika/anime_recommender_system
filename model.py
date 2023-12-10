import pickles

def load_model():
    global anime_rating_model
    global anime_recommendation_model
    anime_rating_model = pickle.load(open('anime_rating_model.sav', 'rb'))
    anime_recommendation_model = pickle.load(open('anime_recommendation_model.sav', 'rb'))
    
