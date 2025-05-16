import streamlit as st
import requests

# Backend API URL
API_URL = "http://localhost:8000"

# Title
st.title("Movie Explorer")

# Show Random Movie Button
if st.button("Show Random Movie"):
    response = requests.get(f"{API_URL}/movies/random/")
    if response.status_code == 200:
        movie = response.json()
        st.session_state["current_movie"] = movie
        st.session_state["summary"] = None
    else:
        st.error("Failed to fetch a random movie.")

# Display Movie Details
if "current_movie" in st.session_state:
    movie = st.session_state["current_movie"]
    st.header(movie["title"])
    st.write(f"Year: {movie['year']}")
    st.write(f"Director: {movie['director']}")
    st.subheader("Actors:")
    for actor in movie["actors"]:
        st.write(f"- {actor['actor_name']}")

# Get Summary Button
if "current_movie" in st.session_state and st.button("Get Summary"):
    movie_id = st.session_state["current_movie"]["id"]
    response = requests.post(f"{API_URL}/generate_summary/", json={"movie_id": movie_id})
    if response.status_code == 200:
        st.session_state["summary"] = response.json()["summary_text"]
    else:
        st.error("Failed to generate a summary.")

# Display Summary
if "summary" in st.session_state and st.session_state["summary"]:
    st.subheader("Summary")
    st.info(st.session_state["summary"])