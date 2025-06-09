
import streamlit as st
import pandas as pd
import numpy as np
import speech_recognition as sr

# Load the mora dataset
@st.cache_data
def load_mora_map():
    df = pd.read_csv("shakes_core_moras_v2.1.csv")
    mora_map = {}
    for _, row in df.iterrows():
        mora = row["Romaji"].strip().lower()
        pattern = row["Rhythmic Pattern"].strip()
        if mora and pattern:
            mora_map[mora] = pattern
    return mora_map

# Define rhythm durations
RHYTHM_DURATION = {
    "s": 100,
    "ŝ": 130,
    "m": 150,
    "ḿ": 170,
    "S": 180,
    "Ś": 200
}

def text_to_moras(text):
    text = text.lower().replace(".", "").replace(",", "")
    moras = [text[i:i+2] for i in range(0, len(text), 2)]
    return moras

def pattern_to_sequence(pattern):
    tokens = pattern.split("-")
    return [(tok, RHYTHM_DURATION.get(tok, 100)) for tok in tokens]

# Speech recognition
@st.cache_resource
def get_recognizer():
    return sr.Recognizer()

def recognize_speech():
    r = get_recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except:
            return ""

# Streamlit UI
st.set_page_config(page_title="Shakes Translator (Cloud)", layout="centered")
st.title("🧠 Shakes Language MVP (Cloud Version)")

mora_map = load_mora_map()

st.write("### Speak or type a phrase below:")

col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("Input text", placeholder="Type something...")
with col2:
    if st.button("🎙️"):
        user_input = recognize_speech()
        st.session_state["speech_input"] = user_input

if "speech_input" in st.session_state and not user_input:
    user_input = st.session_state["speech_input"]
    st.text_input("Input text", value=user_input, key="repeat_input")

if user_input:
    moras = text_to_moras(user_input)
    st.subheader("Detected Moras")
    st.write(moras)

    st.subheader("Vibration Patterns")
    for mora in moras:
        pattern = mora_map.get(mora)
        if pattern:
            st.markdown(f"`{mora}` → {pattern}`")
        else:
            st.warning(f"No pattern found for '{mora}'")

                play_pattern(sequence)
        else:
            st.warning(f"No pattern found for '{mora}'")
