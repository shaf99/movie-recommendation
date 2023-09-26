import streamlit as st
import pickle
import pandas as pd
import requests
# movies_dict = pickle.load(open('movies_dict.pkl','rb'))
# movies = pd.DataFrame(movies_dict)
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    dist = similarity[movie_index]
    movies_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []  # Initialize recommended_movie_names list
    recommended_movie_posters = []  # Initialize recommended_movie_posters list

    for i in movies_list[1:6]:  # Iterate over movies_list
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)


st.title('MOVIE RECOMMENDATION SYSTEM')

similarity = pickle.load(open('similarity.pkl','rb'))
from PIL import Image

image = Image.open(r"C:\Users\shafi\Desktop\banner.jpg")

st.image(image, caption='movies')

selected_movie_name = st.selectbox(
    'Type or select from the list',
    movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    columns = st.columns(5)  # Create 5 columns

    for i in range(5):
        with columns[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
