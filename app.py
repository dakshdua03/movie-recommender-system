import streamlit as st
import pickle
import pandas as pd

# Function to recommend movies
def recommend(movie):
    index = movies_dict[movies_dict['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommendations = [movies_dict.iloc[i[0]].title for i in distances[1:6]]
    return recommendations

# Load the movies and similarity data
movies = pickle.load(open('movies.pkl', 'rb'))
movies_dict = pd.DataFrame(movies)
movies_list = movies_dict['title'].values
similarity = pickle.load(open('nearest_neighbors.pkl', 'rb'))

# Streamlit UI layout
st.set_page_config(page_title="Movie Recommender", page_icon=":clapper:", layout="wide")

st.title('🎬 Movie Recommender')
st.markdown("## Find your next favorite movie!")

# Movie selection
option = st.selectbox('What movie do you want to watch something similar to?', movies_list, index=0)

# Recommendation button
if st.button("Recommend Me"):
    with st.spinner('Finding movies you might like...'):
        recommended_list = recommend(option)
        st.success(f"Movies similar to {option}:")
        for i, title in enumerate(recommended_list, 1):
            st.write(f"{i}. {title}")

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
    Developed by [Daksh Dua](linkedin.com/in/dakshdua03). 
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
    </style>
    <div class="footer">
        © 2024 Movie Recommender App. All rights reserved.
    </div>
    """, unsafe_allow_html=True)
