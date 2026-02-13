from importlib.resources import read_binary
from dotenv import load_dotenv
import os
import time
import streamlit as st
import pickle
import pandas as pd
import requests
import certifi
import ssl

load_dotenv()

# Get your API key
api_key = os.getenv("TMDB_API_KEY")

ssl._create_default_https_context = ssl._create_unverified_context



@st.cache_data
def fetch_poster(movie_id):
    try:
        # wait before sending request (VERY IMPORTANT)
        time.sleep(0.35)

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url, timeout=10)

        # if request failed
        if response.status_code != 200:
            return "https://via.placeholder.com/500x750?text=No+Image"

        data = response.json()

        if data.get('poster_path') is None:
            return "https://via.placeholder.com/500x750?text=No+Image"

        return "https://image.tmdb.org/t/p/w500" + data['poster_path']

    except:
        return "https://via.placeholder.com/500x750?text=No+Image"



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        # correct TMDB movie id
        movie_id = movies.iloc[i[0]]['movie_id']

        print("Fetching:", movies.iloc[i[0]]['title'], "ID:", movie_id)

        # movie name
        recommended_movies.append(movies.iloc[i[0]].title)

        # poster
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters




movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('🎬 AI Movie Recommendation System')
st.write('Get movie recommendations based on content similarity')


selected_movie_name = st.selectbox(
'How would you like to be contacted?',
       movies['title'].values)



if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])



