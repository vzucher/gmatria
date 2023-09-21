import streamlit as st
import pandas as pd
import json
import time
import re

# Set the title and page configuration
st.set_page_config(
    page_title="Gmatria Calculator",
    layout="centered",
)

# Custom CSS
st.markdown("""
<style>
.centered {
    display: flex;
    justify-content: center;
}
.center-text {
    text-align: center !important;
}
td {
    text-align: center !important;
}
.footer {
    text-align: center;
    margin-top: 20px;  /* Add 20px of space above the footer */
</style>
""", unsafe_allow_html=True)


# Load datasets
numerology_file_path = "data/numerology.json"
num_map_df = pd.read_csv('data/num_map_df.csv')

# Load numerology from JSON file
with open(numerology_file_path, 'r') as f:
    numerology = json.load(f)

# Define functions
def gmatria(shoresh, numerology):
    shoresh = shoresh.replace(" ", "")
    shoresh = [*shoresh]
    mapped_array = [numerology[element] for element in shoresh]
    return sum(mapped_array)

def similar_words(gmatria_val, num_map_df):
    return num_map_df[num_map_df['Numerical Value'] == gmatria_val]

# Validate Hebrew input
def is_hebrew(text):
    hebrew_pattern = r'^[א-ת\s]+$'
    return bool(re.match(hebrew_pattern, text))

# Page title
st.title('Gmatria Calculator')

# Input field
input_text = st.text_input("Enter a Hebrew word:", "", max_chars=30)

# Function to create a typing effect
def type_machine(str):
    typed_text = st.empty()
    for i in range(1, len(str) + 1):
        typed_text.markdown(f"<span class='responsive-text'>{str[:i]}</span>", unsafe_allow_html=True)
        time.sleep(0.02)
    time.sleep(1.0)
    typed_text.markdown(f"<span class='responsive-text'>{str}</span>", unsafe_allow_html=True)

# Check for input submission
input_submitted = bool(input_text)

# Validate the input
if input_submitted and not is_hebrew(input_text):
    st.warning("Please enter a valid Hebrew word or phrase.")
elif input_submitted:
    gematria_value = gmatria(input_text, numerology)
    st.success(f"The Gmatria value of '{input_text}' is {gematria_value}")
    df = similar_words(gematria_value, num_map_df)
    df = df.drop(columns=df.columns[0])
    type_machine(str="Here are a few other Shorashim with the same gmatria numerical value:")
    
    # Center and display the DataFrame as HTML
    st.markdown("<div class='centered'><table class='center-text'>" + df.to_html(classes='center-text', index=False) + "</table></div>", unsafe_allow_html=True)

st.empty()
# Add a centered footer
st.markdown("<div class='footer'>All rights reserved by @vzucher</div>", unsafe_allow_html=True)
