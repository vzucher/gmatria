import streamlit as st
import pandas as pd
import json
import time
import re

# Set the title and page configuration
st.set_page_config(
    page_title="Gmatria Calculator",
    layout="wide",  # Use wide layout for better mobile experience
)

# Load datasets
numerology_file_path = "data/numerology.json"
num_map_df = pd.read_csv('data/num_map_df.csv')

# Define functions
def gmatria(shoresh, numerology):
    shoresh = shoresh.replace(" ", "")
    shoresh = [*shoresh]
    mapped_array = [numerology[element] for element in shoresh]
    gmatria_val = sum(mapped_array)
    return gmatria_val

def similar_words(gmatria_val, num_map_df):
    df = num_map_df[num_map_df['Numerical Value'] == gmatria_val]
    return df

# Function to validate Hebrew input
def is_hebrew(text):
    # Regular expression for Hebrew characters
    hebrew_pattern = r'^[א-ת\s]+$'
    return bool(re.match(hebrew_pattern, text))

# Page title
st.title('Gmatria Calculator')

# Input field for Hebrew text
input_text = st.text_input("Enter a Hebrew word:", "", max_chars=30)

# Define a function for typing effect
def type_machine(str):
    typed_text = st.empty()
    for i in range(1, len(str) + 1):
        typed_text.text(str[:i], unsafe_allow_html=True)  # Use unsafe_allow_html to allow HTML tags
        time.sleep(0.02)
    time.sleep(1.0)
    typed_text.text(str, unsafe_allow_html=True)  # Ensure the entire text is displayed

# Check if input is submitted
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
    df = similar_words(gmatria_value, num_map_df)
    df = df.drop(columns=df.columns[0])
    type_machine(str="Here are a few other Shorashim with the same gmatria numerical value:<br><br>")
    st.dataframe(df)

# Add footer
st.text('All rights reserved by @vzucher')
