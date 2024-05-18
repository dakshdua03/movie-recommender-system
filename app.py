import streamlit as st
import pickle
import pandas as pd
import requests

# Set page configuration
st.set_page_config(page_title="Movie Recommender", page_icon=":clapper:", layout="wide")

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Function to recommend movies
def recommend(movie):
    index = movies_dict[movies_dict['title'] == movie].index[0]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in similarity[index]:
        movie_id = movies_dict.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies_dict.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


# Load the movies and similarity data
try:
    movies = pickle.load(open('movies.pkl', 'rb'))
    movies_dict = pd.DataFrame(movies)
    movies_list = movies_dict['title'].values
    similarity = pickle.load(open('nearest_neighbors.pkl', 'rb'))
except FileNotFoundError as e:
    st.error(f"File not found: {e.filename}")
except Exception as e:
    st.error(f"An error occurred while loading data: {e}")

if 'similarity' not in locals():
    st.error("The similarity data could not be loaded. Please check the 'nearest_neighbors.pkl' file.")
else:
    # Streamlit UI layout
    st.title('🎬 Movie Recommender')
    st.markdown("## Find your next favorite movie!")

    # Movie selection
    option = st.selectbox('What movie do you want to watch something similar to?', movies_list, index=0)

    # Recommendation button
    if st.button("Recommend Me"):
        with st.spinner('Finding movies you might like...'):
            recommended_names, recommended_posters = recommend(option)
            st.success(f"Movies similar to {option}:")

            # Display recommendations in one row
            cols = st.columns(5)
            for col, name, poster in zip(cols, recommended_names, recommended_posters):
                with col:
                    st.text(name)
                    st.image(poster, width=150)

    # Sidebar with additional information
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This is a movie recommender app built with Streamlit. 
        Select a movie you like and get recommendations for similar movies.
        """
    )
    st.sidebar.title("Developer")
    st.sidebar.info(
        """
        Developed by [Daksh Dua](https://www.linkedin.com/in/dakshdua03/). 
        Feel free to connect!
        """
    )

    # Footer with a disclaimer or additional links
    st.markdown("""
        <style>
            .footer {
                position: fixed;
                bottom: 0;
                width: 100%;
                background-color: #f1f1f1;
                color: #000;
                text-align: center;
                padding: 10px;
                font-size: 14px;
            }
            .element-container img {
                border-radius: 10px;
                width: 100%; /* Ensure images fit within their columns */
            }
        </style>
        <div class="footer">
            © 2024 Movie Recommender App. All rights reserved.
        </div>
        """, unsafe_allow_html=True)
