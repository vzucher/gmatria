from names_dataset import NameDataset
from googletrans import Translator
from nltk.corpus import words
import streamlit as st
import pandas as pd
import json
import nltk
import time
import re

# Set the title and page configuration
st.set_page_config(
    page_title="Gmatria Calculator",
    layout="centered",
)

# Custom CSS
# Custom CSS
# Custom CSS
# Custom CSS
st.markdown("""
<style>
.center-text {
    text-align: center !important;
}
td, th {
    text-align: center !important;
}
.dataframe-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 100%;
}
.footer {
    text-align: center;
    margin-top: 20px;  /* Add 20px of space above the footer */
}
</style>
""", unsafe_allow_html=True)



# Page title
st.title('Gmatria Calculator')

st.write('<div class="dataframe-container"></div>', unsafe_allow_html=True)

# Input field
input_text = st.text_input("Enter a Hebrew or English word or phrase:", "", max_chars=30)

# Load datasets
numerology_file_path = "data/numerology.json"
dic = pd.read_csv('data/dic.csv')

# Load numerology from JSON file
with open(numerology_file_path, 'r') as f:
    numerology = json.load(f)

# Validate Hebrew input
def is_hebrew(text):
    hebrew_pattern = r'^[א-ת\s]+$'
    return bool(re.match(hebrew_pattern, text))

def is_name(text):
    nd = NameDataset()
    check = nd.search(text) != None
    return check

nltk.download('words', force=True)
word_list = set(words.words())

def is_english(phrase):
    # Split the phrase into individual words
    words_in_phrase = phrase.split()
    
    # Check if each word is in the English word list
    return all(word.lower() in word_list for word in words_in_phrase)

def translate(string):
    string = translator.translate(string, dest="he", src="en").text
    return string

def remove_nekudot(text):
    # Use a regular expression to remove all Hebrew vowel points
    cleaned_text = re.sub(r'[\u0591-\u05BD\u05BF-\u05C2\u05C4-\u05C7\u05F3\u05F4]', '', text)
    return cleaned_text

# Define functions
def gmatria(word, numerology):
    
    word = word.replace(" ", "")
    word = [*word]
    mapped_array = [numerology[element] for element in word]
    return sum(mapped_array)

def similar_words(gmatria_val, dic):
    return dic[dic['Gmatria Value'] == gmatria_val]


# Function to create a typing effect
def type_machine(str):
    typed_text = st.empty()
    for i in range(1, len(str) + 1):
        typed_text.markdown(f"<span class='responsive-text'>{str[:i]}</span>", unsafe_allow_html=True)
        time.sleep(0.02)
    time.sleep(1.0)
    typed_text.markdown(f"<span class='responsive-text'>{str}</span>", unsafe_allow_html=True)

#     # Center and display the DataFrame as HTML
#     st.markdown("<div class='centered'><table class='center-text'>" + df.to_html(classes='center-text', index=False) + "</table></div>", unsafe_allow_html=True)

def display_df(gval):
    df = similar_words(gval, dic)
    df = df.drop(columns=df.columns[0])
    filtered_df = st.dataframe(df)
    return filtered_df
        
def calculator(input_text, numerology, dic):

    # If no input provided, just return
    if not input_text:
        return

    # If it's a Hebrew word
    if is_hebrew(input_text):
        gematria_value = gmatria(input_text, numerology)
        st.success(f"The Gmatria value of '{input_text}' is {gematria_value}")
        df = similar_words(gematria_value, dic)
        df = df.drop(columns=df.columns[0])
        type_machine(str="Here are a few other Shorashim with the same gmatria numerical value:")
        display_df(gematria_value)
        
    elif is_name(input_text):
        translator = Translator()
        translated_text = translator.translate(input_text, src='en', dest='he').text
        gematria_value = gmatria(translated_text, numerology)
        st.success(f"The Gmatria value of the name '{input_text}' is {gematria_value}")
        df = similar_words(gematria_value, dic)
        df = df.drop(columns=df.columns[0])
        type_machine(str="Here are a few other words in Hebrew with the same gmatria numerical value:")
        display_df(gematria_value)
        
    # If it's an English word
    elif is_english(input_text):
        translator = Translator()
        translated_text = translator.translate(input_text, src='en', dest='he').text
        translated_text = remove_nekudot(translated_text)
        gematria_value = gmatria(translated_text, numerology)
        st.success(f"The Gmatria value of '{translated_text}' (translated from '{input_text}') is {gematria_value}")
        df = similar_words(gematria_value, dic)
        df = df.drop(columns=df.columns[0])
        type_machine(str="Here are a few other words in Hebrew with the same gmatria numerical value:")
        display_df(gematria_value)


    # If input isn't valid Hebrew or English
    else:
        st.warning("Please enter a valid Hebrew or English word or phrase.")
        
        
calculator(input_text, numerology, dic)

# Add a centered footer
st.markdown("<div class='footer'>All rights reserved by @vzucher</div>", unsafe_allow_html=True)