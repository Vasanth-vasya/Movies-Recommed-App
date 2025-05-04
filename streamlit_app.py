
import streamlit as st
import pickle
import requests
import urllib.request
import streamlit as st
import os



file_path = 'sim.pkl'
file_url = 'https://drive.google.com/file/d/1Avu4KJ6iuNy4Sd8CoUVJn6ZpqC9ScMhw/view?usp=sharing'

with open('sim.pkl', 'rb') as f:
    sim = pickle.load(f)


# Download if not exists
if not os.path.exists(file_path):
    with st.spinner('Downloading sim.pkl...'):
        urllib.request.urlretrieve(file_url, file_path)

# Now load it
with open(file_path, 'rb') as f:
    sim = pickle.load(f)

# Load movie data and similarity matrix
movies = pickle.load(open('movies_list.pkl', 'rb'))
sim = pickle.load(open('sim.pkl', 'rb'))

# Get list of movie titles
movies_list = movies['title'].values

# Streamlit app title
st.header('🎬 Movie Recommender System')

# TMDb API key
API_KEY = '5fe2fe423f8c051cc56fece422313853'

# Movie selection dropdown
select_values = st.selectbox("🎥 Select a Movie", movies_list)

# Fetch movie poster using TMDb API
def fetch_poster(movie_title):
    try:
        # ✅ Correct URL formatting with f-string
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
        data = requests.get(url).json()
        
        # ✅ Check if 'results' and 'poster_path' are present
        if data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        pass
    
    # Fallback image if poster not found
    return "https://via.placeholder.com/200x300?text=No+Image"

# Recommend similar movies based on similarity matrix
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(sim[index])), reverse=True, key=lambda vec: vec[1])

    recommend_movie = []
    for i in distance[1:6]:  # Get top 5 recommendations
        recommend_movie.append(movies.iloc[i[0]].title)
    
    return recommend_movie

# Show recommendations when button is clicked
if st.button("Show Recommends"):
    movies_name = recommend(select_values)
    cols = st.columns(5)

    # ✅ Loop through available movies to avoid IndexError
    for i in range(len(movies_name)):
        with cols[i]:
            st.text(movies_name[i])  # Movie title
            st.image(fetch_poster(movies_name[i]), use_container_width=True)
