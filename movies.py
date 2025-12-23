import streamlit as st
import pickle
import pandas as pd
import requests

# Page configuration
st.set_page_config(page_title="CineSync", page_icon="🎬", layout="wide")

# Custom CSS for beige and violet theme
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #F5F5DC;
    }
    
    /* Title styling */
    h1 {
        color: #6B2C91;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(107, 44, 145, 0.2);
    }
    
    /* Selectbox styling */
    .stSelectbox label {
        color: #6B2C91 !important;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #6B2C91;
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        border: none;
        box-shadow: 0 4px 6px rgba(107, 44, 145, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #8B3CB8;
        box-shadow: 0 6px 12px rgba(107, 44, 145, 0.4);
        transform: translateY(-2px);
    }
    
    /* Movie title text */
    .stText {
        color: #6B2C91;
        font-weight: 600;
    }
    
    /* Column styling */
    [data-testid="column"] {
        background-color: rgba(255, 255, 255, 0.6);
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(107, 44, 145, 0.15);
        transition: transform 0.2s;
    }
    
    [data-testid="column"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(107, 44, 145, 0.25);
    }
    
    /* Image styling */
    img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Selectbox dropdown */
    [data-baseweb="select"] {
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)

def fetch(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    recommended_movies = []
    poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster.append(fetch(movie_id))
    return recommended_movies, poster

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Header
st.markdown("<h1> CineSync</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B2C91; font-size: 1.3rem; margin-bottom: 2rem;'>Your Personal Movie Recommendation System</p>", unsafe_allow_html=True)

# Movie selection
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_movie_name = st.selectbox(
        "What movie would you like recommendations for?",
        movies['title'].values
    )
    
    recommend_button = st.button(' Get Recommendations', use_container_width=True)

# Display recommendations
if recommend_button:
    with st.spinner('Finding perfect matches...'):
        names, posters = recommend(selected_movie_name)
    
    st.markdown("<h2 style='color: #6B2C91; text-align: center; margin-top: 2rem; margin-bottom: 1.5rem;'>Recommended Movies For You</h2>", unsafe_allow_html=True)
    
    # First row - 5 movies
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx], use_container_width=True)
    
    # Second row - 5 movies
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx + 5])
            st.image(posters[idx + 5], use_container_width=True)
