import streamlit as st
import pickle
import pandas as pd
import requests

def fetch(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]

    recommened_movies=[]
    poster=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommened_movies.append(movies.iloc[i[0]].title)
        poster.append(fetch(movie_id))
    return recommened_movies,poster

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))
st.title('CineSync : A Movie Recommendation System')
selected_movie_name = st.selectbox("What is the movie in your checklist",movies['title'].values)
if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)

    c1,c2,c3,c4,c5,c6,c7,c8,c9,c10= st.columns(10)

    with c1:
      st.text(names[0])
      st.image(posters[0])
    with c2:
      st.text(names[1])
      st.image(posters[1])
    with c3:
      st.text(names[2])
      st.image(posters[2])
    with c4:
      st.text(names[3])
      st.image(posters[3])
    with c5:
      st.text(names[4])
      st.image(posters[4])
    with c6:
      st.text(names[5])
      st.image(posters[5])
    with c7:
      st.text(names[6])
      st.image(posters[6])
    with c8:
      st.text(names[7])
      st.image(posters[7])
    with c9:
      st.text(names[8])
      st.image(posters[8])
    with c10:
      st.text(names[9])
      st.image(posters[9])