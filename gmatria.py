import streamlit as st
import pandas as pd
import numpy as np
import json
import time
import re

st.title('Gmatria Calculator')

# Load datasets

# numerology

numerology_file_path = "data/numerology.json"

# Load the JSON data from the file
with open(numerology_file_path, "r") as json_file:
    numerology = json.load(json_file)
    
# num_map_df

num_map_df = pd.read_csv('data/num_map_df.csv')
    
def gmatria(shoresh, numerology):
    
    shoresh = shoresh.replace(" ", "")
    shoresh = [*shoresh]
    mapped_array = [numerology[element] for element in shoresh]
    gmatria_val = sum(mapped_array)
    return gmatria_val

def each_letter_value(shoresh, numerology):
    arr_arr = []
    shoresh = [*shoresh]
    mapped_array = [numerology[element] for element in shoresh]
    arr_arr.append(mapped_array)
    return arr_arr

def similar_words(gmatria_val, num_map_df):
    df = num_map_df[num_map_df['Numerical Value'] == gmatria_val]
    return df


# Function to validate Hebrew input

def is_hebrew(text):
    # Regular expression for Hebrew characters
    hebrew_pattern = r'^[א-ת\s]+$'
    return bool(re.match(hebrew_pattern, text))

label = 'Search Numerical Value of the Hebrew Word:'

# st.text_input(label, max_chars=140)

# Input field for Hebrew text
input_text = st.text_input("Enter a Hebrew word:", "",max_chars=30)
str = "Here are a few other Shorashim with the same gmatria numerical value:"

def type_machine(str):

    typed_text = st.empty()
    # Typing effect
    for i in range(1, len(str) + 1):
        typed_text.text(str[:i])
        time.sleep(0.02)  # Adjust the sleep duration for typing speed
    # Add a delay before displaying the entire text
    time.sleep(1.0)
    # Display the entire text without typing effect
    typed_text.text(str)
    
if input_text:
    input_submitted = True
else:
    input_submitted = False

# Validate the input if it has been submitted
if input_submitted and not is_hebrew(input_text):
    st.warning("Please enter a valid Hebrew word or phrase.")
elif input_submitted:
    # Calculate gematria value
    gematria_value = gmatria(input_text, numerology)
    st.success(f"The Gmatria value of '{input_text}' is {gematria_value}")
    df = similar_words(gematria_value, num_map_df)
    df = df.drop(columns=df.columns[0])
    type_machine(str)
    st.dataframe(df)

st.text('all rights reserved by @vzucher')
