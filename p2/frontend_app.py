import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="Product Review & Recommendation System", page_icon="🔍", layout="centered")

# Title and description
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🔍 Product Review & Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Use this app to generate product reviews, get product recommendations, and summarize product features.</p>", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
function = st.sidebar.selectbox("Select Function", ["Make Review", "Pointwise Recommender", "Pairwise Recommender", "Listwise Recommender", "Summarize Product Features"])

# Function to display and handle inputs
def display_function(function):
    if function == "Make Review":
        st.markdown("<h2 style='color: #4CAF50;'>Make Review</h2>", unsafe_allow_html=True)
        product_id = st.text_input("Product ID", placeholder="Enter Product ID")
        if st.button("Submit"):
            response = requests.post("http://localhost:8001/make_review", json={"product_id": product_id})
            st.write(response.json())

    elif function == "Pointwise Recommender":
        st.markdown("<h2 style='color: #4CAF50;'>Pointwise Recommender</h2>", unsafe_allow_html=True)
        user_id = st.text_input("User ID", placeholder="Enter User ID")
        product_id = st.text_input("Product ID", placeholder="Enter Product ID")
        if st.button("Submit"):
            response = requests.post("http://localhost:8001/pointwise_recommender", json={"user_id": user_id, "product_id": product_id})
            st.write(response.json())

    elif function == "Pairwise Recommender":
        st.markdown("<h2 style='color: #4CAF50;'>Pairwise Recommender</h2>", unsafe_allow_html=True)
        user_id = st.text_input("User ID", placeholder="Enter User ID")
        product_id1 = st.text_input("Product ID 1", placeholder="Enter First Product ID")
        product_id2 = st.text_input("Product ID 2", placeholder="Enter Second Product ID")
        if st.button("Submit"):
            response = requests.post("http://localhost:8001/pairwise_recommender", json={"user_id": user_id, "product_id1": product_id1, "product_id2": product_id2})
            st.write(response.json())

    elif function == "Listwise Recommender":
        st.markdown("<h2 style='color: #4CAF50;'>Listwise Recommender</h2>", unsafe_allow_html=True)
        user_id = st.text_input("User ID", placeholder="Enter User ID")
        product_ids = st.text_input("Product IDs (comma separated)", placeholder="Enter Product IDs separated by commas")
        product_ids_list = [pid.strip() for pid in product_ids.split(',')]
        if st.button("Submit"):
            response = requests.post("http://localhost:8001/listwise_recommender", json={"user_id": user_id, "product_ids": product_ids_list})
            st.write(response.json())

    elif function == "Summarize Product Features":
        st.markdown("<h2 style='color: #4CAF50;'>Summarize Product Features</h2>", unsafe_allow_html=True)
        product_id = st.text_input("Product ID", placeholder="Enter Product ID")
        if st.button("Submit"):
            response = requests.post("http://localhost:8001/summarize_product_features", json={"product_id": product_id})
            st.write(response.json())

# Display the selected function
display_function(function)
