import streamlit as st
import pandas as pd
import numpy as np
import math
from PIL import Image
import pickle
import joblib
import random

from sklearn.base import BaseEstimator, TransformerMixin

class CustomRemover(BaseEstimator, TransformerMixin):

    def __init__(self, useless_attribs):
        self.useless_attribs = useless_attribs

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()

        X_copy = X_copy.drop(self.useless_attribs, axis=1)

        return X_copy

full_pipeline = joblib.load('pipeline.joblib')

with open("model.pkl", 'rb') as file:
    clf = pickle.load(file)

st.title('If You Were a Superhero, Would You Be GOOD, NEUTRAL, or BAD?!?!')
 
DATA = 'heroes_information.csv'
POWERS = 'super_hero_powers.csv'

@st.cache
def load_data(file):
    data = pd.read_csv(file)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

# Filter dataframe for top closest to user inputted data
def closest(data, gender, eye_color, race, hair_color, height, publisher, skin_color, weight, top=3):
    filtered = data.loc[(data["gender"] == gender)
            & (data["eye color"] == eye_color)
            & (data["race"] == race)
            & (data["hair color"] == hair_color)
            & (data["publisher"] == publisher)
            & (data["skin color"] == skin_color)]
    if len(filtered) < top:
        filtered = data.loc[(data["gender"] == gender)
            & (data["eye color"] == eye_color)
            & (data["race"] == race)
            & (data["hair color"] == hair_color)
            & (data["publisher"] == publisher)]
        if len(filtered) < top:
            filtered = data.loc[(data["gender"] == gender)
            & (data["eye color"] == eye_color)
            & (data["race"] == race)
            & (data["hair color"] == hair_color)]
            if len(filtered) < top:
                filtered = data.loc[(data["gender"] == gender)
                & (data["eye color"] == eye_color)
                & (data["race"] == race)]
                if len(filtered) < top:
                    filtered = data.loc[(data["gender"] == gender)
                    & (data["eye color"] == eye_color)]
                    if len(filtered) < top:
                        filtered = data.loc[(data["gender"] == gender)]
    return filtered

# Create a text element and show that data is loading
data_load_state = st.text("Loading data...")
# Load 100 rows of data into the dataframe
data = load_data(DATA)
powers = load_data(POWERS)
# Show that data was successfully loaded
data_load_state.text('Loading data complete!!!')

st.write("Raw Data from Super Heroes Dataset from https://www.kaggle.com/datasets/claudiodavi/superhero-set")
st.write(data)

# Get data inputs from user
# Gender, eye color, race, hair color, height, skin color, weight
# To do: order better, set default values?
st.sidebar.subheader("Enter Your Information Here!")

name = st.sidebar.text_input("What is your superhero name?", placeholder ="Enter")

unnamed = st.sidebar.text_input("What is your sidekick's name?", placeholder ="Enter")

gender = st.sidebar.selectbox("What is your gender?", data["gender"].drop_duplicates())

eye_color = st.sidebar.selectbox("What is your eye color?", data["eye color"].drop_duplicates())

race = st.sidebar.selectbox("What is your race?", data["race"].drop_duplicates())

hair_color = st.sidebar.selectbox("What is your hair color?", data["hair color"].drop_duplicates())

max_height = int(data["height"].max())
min_height = 0
height = st.sidebar.slider("What is your height in centimenters?", min_height, max_height, int((min_height+max_height)/2))

publisher = st.sidebar.selectbox("What is your favorite publisher?", data["publisher"].drop_duplicates())

skin_color = st.sidebar.selectbox("What is your skin color?", data["skin color"].drop_duplicates())

max_weight = int(data["weight"].max()) 
min_weight = 0
weight = st.sidebar.slider("What is your weight in pounds?", min_weight, max_weight, int((min_weight+max_weight)/2))

# Data frame containing user input (no unnamed or name or alignment)
# TO DO: Need to modify this structure here so it's correct to pass into the model
# add unnamed and name to user_data --> added
user_data = pd.DataFrame(np.array([[unnamed, name, gender, eye_color, race, hair_color, height, publisher, skin_color, weight]]),
columns = ["unnamed: 0", "name", "gender", "eye color", "race", "hair color", "height", "publisher", "skin color", "weight"])
st.subheader("User input:")
st.write(user_data)

# user_input_prepared = pd.DataFrame(user_data, columns =['Unnamed: 0', 'name', 'Gender', 'Eye color', 'Race', 'Hair color', 'Height', 'Publisher', 'Skin color', 'Weight'])
# user_input_prepared = full_pipeline.transform(user_input_prepared)
# user_prediction = clf.predict(user_input_prepared)
user_prediction = random.randrange(0,1,2)

if 'number_submitted' not in st.session_state:
    st.session_state.number_submitted = 0

submit = st.button("Calculate my superhero affinity!")

st.write("Number of Hack Clubbers Who Have Demoed Our Project: "+str(st.session_state.number_submitted))

if submit:
    if user_prediction == 0:
        alignment = "BAD"
        image = Image.open('assets/bad.jpeg')
    elif user_prediction == 1:
        alignment = "GOOD"
        image = Image.open('assets/good.jpeg')
    else:
        alignment = "NEUTRAL"
        image = Image.open('assets/neutral.jpeg')
    st.session_state.number_submitted+=1
    
    st.subheader("Here's the verdict...")

    st.write("Your alignment is...")
    st.subheader(alignment)
    st.image(image)

    # Retrieve closest 3 matches to what the user inputted and display
    search = closest(data, gender, eye_color, race, hair_color, height, publisher, skin_color, weight, top=3)

    st.write("And these are the top 3 superheroes who are most similar to you!")
    st.write(search)

    # To do: improve this section by only showing the cells that are True?
    st.write("These are some powers that would suit you based on these similar superheroes!")
    matches = search["name"]
    for match in matches:
        row_to_check = powers.loc[(powers["hero_names"] == match)]
        st.write(row_to_check)
