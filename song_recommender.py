import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# config
st.set_page_config(page_title="🎵 Song Recommender", layout="centered")
st.title("🎵 Song Recommender")
st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <h1 style="font-size: 48px;">🎶 Song Vibes</h1>
    <p style="font-size: 18px; color: gray;">Tell us your vibe and we'll find your next favourite tracks</p>
</div>
 """, unsafe_allow_html=True)

 with st.form("prompt_form"):
    user_input = st.text_input("🎧 What's your vibe?", placeholder="e.g., mellow beach evening, heartbreak, gym pump-up")
    submitted = st.form_submit_button("Get Recommendations")

for name, artist, url, cover in spotify_tracks:
    with st.container():
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 20px; padding: 10px; border-radius: 10px;
                background-color: #f8f9fa; box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
            <img src="{cover}" width="80"
        )
# api keys
genai.configure(api_key="AIzaSyAAJpxsjVsODYvYf6B5ow3GiHzQrbLvAFE")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="8b06976fab42432fa7486a5a866d01b9",
    client_secret="06a2761ac7a34c758a77856a6ec42531"
))


def get_recommendations(prompt):
    """Ask Gemini to suggest songs based on a mood or theme."""
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
        f"You are a song recommendation engine. Suggest a list of 5 songs based on this: {prompt}. Give the song and artist names only."
    )
    return response.text

def search_spotify_songs(recommendation_text):
    tracks = []
    lines = recommendation_text.strip().split("\n")

    for line in lines:
        # Try to extract song name and artist
        if " - " in line:
            name, artist = line.split(" - ", 1)
        elif " by " in line:
            name, artist = line.split(" by ", 1)
        else:
            continue  # skip if format is off

        query = f"{name} {artist}"
        result = sp.search(q=query, limit=1, type="track")
        items = result["tracks"]["items"]

        if items:
            track = items[0]
            song_url = track["external_urls"]["spotify"]
            cover_art = track["album"]["images"][0]["url"]
            tracks.append((name.strip(), artist.strip(), song_url, cover_art))
    return tracks

def get_song_description(song, artist):
    """Generate a 1-2 line description of the song using Gemini."""
    prompt = f"Give a short, 1-2 line description of the song '{song}' by {artist}. Don't include release year or chart info."
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text.strip()

def spotify_button(url):
    """HTML button styled like Spotify."""
    return f"""
    <a href="{url}" target="_blank">
        <button style='padding: 6px 12px; background-color: #1DB954; 
                       color: white; border: none; border-radius: 5px;
                       font-size: 14px; cursor: pointer;'>
            🎧 Listen on Spotify
        </button>
    </a>
    """

#UI

user_input = st.text_input("What are you in the mood for? (e.g., chill sunset drive, late night coding, heartbreak, etc.)")

if user_input:
    with st.spinner("Getting personalized recommendations..."):
        rec_text = get_recommendations(user_input)
        spotify_tracks = search_spotify_songs(rec_text)

    if spotify_tracks:
        st.markdown("## 🔥 Your Recommended Tracks")
        for name, artist, url, cover in spotify_tracks:
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.image(cover, width=80)
                with col2:
                    st.markdown(f"### {name}")
                    st.markdown(f"**Artist**: {artist}")
                    description = get_song_description(name, artist)
                    st.markdown(f"*{description}*")
                    st.markdown(spotify_button(url), unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.error("Couldn’t find any tracks on Spotify for those recommendations. Try changing your prompt.")
