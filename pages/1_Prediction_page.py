import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
from PIL import Image
from io import BytesIO


# Load data
@st.cache_data
def load_data():
    return pd.read_pickle('data/laptop_data.pkl')


# Preprocess data
def preprocess_data(data):
    features = ['brand', 'processor', 'CPU', 'Ram', 'Ram_type', 'ROM', 'ROM_type', 'GPU',
                'display_size', 'resolution_width', 'resolution_height', 'OS', 'warranty']
    for feature in features:
        data[feature] = data[feature].astype(str)
    data['description'] = data[features].apply(lambda x: ' '.join(x), axis=1)
    return data


# Compute similarity matrix
@st.cache_data
def compute_similarity_matrix(data):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['description'])
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return similarity_matrix






# Recommend laptops based on model and specs
def recommend_laptops(selected_laptop, similarity_matrix, data):
    # Preprocess selected laptop's specs
    selected_laptop = ' '.join(selected_laptop.values())

    # Compute similarity scores
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform([selected_laptop] + list(data['description']))
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

    # Get indices of similar laptops
    similar_laptops_indices = similarity_scores.argsort()[::-1][1:4]  # Top 3 similar laptops

    # Get similar laptops data
    similar_laptops_data = data.iloc[similar_laptops_indices]

    return similar_laptops_data


# Main function
def main():
    st.set_page_config("Prediction", "🔻", "centered", "expanded")
    st.header("Laptop Recommendation System", divider="blue")
    
    # Load data
    data = load_data()

    # Preprocess data
    data = preprocess_data(data)

    # Compute similarity matrix
    similarity_matrix = compute_similarity_matrix(data)

    # Page navigation
    page = st.sidebar.radio("Navigation", ["Input", "Prediction"])

    if page == "Input":
        st.sidebar.title("Select Laptop Model and Specifications")

        with st.form("input_form"):
            col1, col2 = st.columns(2)
            with col1:
                selected_laptop = {}
                selected_laptop['Brand'] = st.selectbox("Brand", data['brand'].unique())
                selected_laptop['Processor'] = st.selectbox("Processor", data['processor'].unique())
                selected_laptop['RAM'] = st.selectbox("RAM", data['Ram'].unique())
                selected_laptop["GPU"] = st.selectbox("graphic card",data["GPU"].unique())
            with col2:
                selected_laptop['Storage'] = st.selectbox("Storage", data['ROM'].unique())
                selected_laptop['Display Size'] = st.selectbox("Display Size", data['display_size'].unique())
                selected_laptop['Operating System'] = st.selectbox("Operating System", data['OS'].unique())
            submitted = st.form_submit_button("Input")

        if submitted:
            st.session_state.selected_laptop = selected_laptop
            st.info("Input Submitted. Click on 'Prediction' to see recommendations.")

    elif page == "Prediction":
        selected_laptop = st.session_state.selected_laptop
        st.sidebar.subheader("Selected Laptop Specs:")
        for key, value in selected_laptop.items():
            st.sidebar.write(f"{key}: {value}")

        # Recommend laptops
        if selected_laptop is not None:
            recommended_laptops = recommend_laptops(selected_laptop, similarity_matrix, data)

            # Display recommendations
            if not recommended_laptops.empty:
                for i, laptop in recommended_laptops.iterrows():
                    # Display image and specifications in columns
                    col1, col2, col3 = st.columns(([5,0.1,1]))
                    with col3:
                        st.image(laptop['image'], width=200)
                    with col2:
                        st.text(" ")
                    with col1:
                        laptop_specs = f"model: {laptop['brand']} {laptop['name']}\n"\
                                       f"graphic card: {laptop['GPU']}\n"\
                                       f"Processor: {laptop['processor']}\n" \
                                       f"RAM: {laptop['Ram']} ,Storage: {laptop['ROM']}\n"\
                                       f"Display Size: {laptop['display_size']}\n" \
                                       f"Resolution: {laptop['resolution_width']} x {laptop['resolution_height']}\n" \
                                       f"Operating System: {laptop['OS']}\n" \
                                       f"Warranty: {laptop['warranty']}\n"\
                                       f"price: ₹{laptop['price']}\n"\
                                       
                        st.text(laptop_specs)
                        # Add spacing between image and specs columns
                        st.write("<div style='height:50px'></div>", unsafe_allow_html=True)

            else:
                st.write("No similar laptops found.")


if __name__ == "__main__":
    main()