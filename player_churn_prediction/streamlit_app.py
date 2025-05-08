import streamlit as st
import joblib
import numpy as np
import warnings  # added for warning suppression
import gdown
import os


# Google Drive file IDs
MODEL_URL_ID = "1umhIDybDcx9RyF-iBAYcJocAWJhHaGqW"
ENCODER_URL_ID = "1LPFDbaHAx1of39nJ-VeMNRav7q2cSd4K"

# Paths
MODEL_PATH = "best_rf_model.pkl"
ENCODER_PATH = "label_encoder.pkl"

# Download if not present
if not os.path.exists(MODEL_PATH):
    gdown.download(id=MODEL_URL_ID, output=MODEL_PATH, quiet=False)

if not os.path.exists(ENCODER_PATH):
    gdown.download(id=ENCODER_URL_ID, output=ENCODER_PATH, quiet=False)

# Load files
model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

st.title("🎮 Player Engagement Level Predictor")

st.markdown("Fill out the player profile below to predict their engagement level.")

# User inputs
age = st.slider("Age", 10, 60, 25)
play_time = st.slider("Avg Play Time per Session (Hours)", 0.0, 20.0, 5.0)
in_game_purchase = st.selectbox("In-Game Purchases", [0, 1])
difficulty = st.selectbox("Game Difficulty", ['Easy', 'Medium', 'Hard'])
sessions_per_week = st.slider("Sessions Per Week", 1, 30, 5)
avg_duration = st.slider("Avg Session Duration (mins)", 10, 300, 90)
level = st.slider("Player Level", 1, 100, 20)
achievements = st.slider("Achievements Unlocked", 0, 100, 10)

# One-hot encoding for categorical features (GameDifficulty)
difficulty_map = {'Easy': [1, 0, 0], 'Medium': [0, 1, 0], 'Hard': [0, 0, 1]}
difficulty_encoded = difficulty_map[difficulty]

# Gender encoding (assuming male = 1, female = 0)
gender_male = st.selectbox("Gender (Male = 1, Female = 0)", [0, 1])

# Location encoding (assuming 3 locations: Europe, Other, USA)
location_europe = st.selectbox("Location (Europe = 1, Other = 0, USA = 0)", [0, 1])
location_other = st.selectbox("Location (Other = 1, Europe = 0, USA = 0)", [0, 1])

# Game Genre encoding (assuming 7 genres, excluding game_genre_strategy)
game_genre_rpg = st.selectbox("Game Genre (RPG = 1, Other = 0)", [0, 1])
game_genre_simulation = st.selectbox("Game Genre (Simulation = 1, Other = 0)", [0, 1])
game_genre_sports = st.selectbox("Game Genre (Sports = 1, Other = 0)", [0, 1])

# Combine inputs into a single list (ensure order matches the features used during training)
input_data = np.array([[age, play_time, in_game_purchase, sessions_per_week, avg_duration, level, achievements] + 
                       difficulty_encoded + 
                       [gender_male] + 
                       [location_europe, location_other] + 
                       [game_genre_rpg, game_genre_simulation, game_genre_sports]])  # Now 16 features

# Debug: Print input_data shape
st.write(f"Input Data Shape: {input_data.shape}")

# Check that the input data has 16 features (this should match the model's expectation)
assert input_data.shape[1] == 16, f"Expected 16 features, but got {input_data.shape[1]} features."

# Skip scaling, use raw input data directly
input_scaled = input_data  # No scaling needed, use raw input data

# Prediction
if st.button("Predict Engagement Level"):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        
    pred = model.predict(input_scaled)
    pred_label = label_encoder.inverse_transform(pred)[0]
    st.success(f"🎯 Predicted Engagement Level: **{pred_label}**")
