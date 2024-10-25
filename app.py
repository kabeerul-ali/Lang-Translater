import os
import requests
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Load Azure credentials from .env
TRANSLATOR_KEY = os.getenv("TRANSLATOR_KEY")
TRANSLATOR_ENDPOINT = os.getenv("TRANSLATOR_ENDPOINT")
TRANSLATOR_LOCATION = os.getenv("TRANSLATOR_LOCATION")

# Supported languages (can be expanded as needed)
supported_languages = {
    'en': 'English',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh-Hans': 'Chinese (Simplified)',
    'ru': 'Russian',
    'pt': 'Portuguese',
    'hi': 'Hindi'   
}

# Function to translate text using Azure Translator
def translate_text(text, target_language):
    path = '/translate?api-version=3.0'
    params = f'&to={target_language}'
    constructed_url = TRANSLATOR_ENDPOINT + path + params
    
    headers = {
        'Ocp-Apim-Subscription-Key': TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': TRANSLATOR_LOCATION,
        'Content-type': 'application/json'
    }
    
    body = [{'text': text}]
    
    response = requests.post(constructed_url, headers=headers, json=body)
    response.raise_for_status()  # Raise an error for bad responses
    translation = response.json()
    
    translated_text = translation[0]['translations'][0]['text']
    return translated_text

# Streamlit App
st.title("TranslinguaX: Empowering Global Communication with Azure")

# Initialize session state for text and output language
if 'text' not in st.session_state:
    st.session_state.text = ''
if 'target_language' not in st.session_state:
    st.session_state.target_language = 'fr'  # Default target language
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ''

# Input text (increased size with text_area)
text = st.text_area("Enter the text to translate:", value=st.session_state.text, height=150)
st.session_state.text = text

# Language selection for target language
target_language = st.selectbox("Select target language:", list(supported_languages.keys()), 
                                format_func=lambda x: supported_languages[x], 
                                index=list(supported_languages.keys()).index(st.session_state.target_language))
st.session_state.target_language = target_language

# Layout for buttons
col1, col2 = st.columns([9, 1])  # Adjust column widths to space out buttons

# Translate button in the first column
with col1:
    if st.button("Translate"):
        if text:
            translated_text = translate_text(text, target_language)
            st.session_state.translated_text = translated_text
            st.text_area("Translated Text:", value=st.session_state.translated_text, height=150, key='output_area', label_visibility="visible")
        else:
            st.error("Please enter text to translate.")

# Clear button in the second column (right aligned)
with col2:
    if st.button("Clear"):
        # Clear the session state values
        st.session_state.text = ''
        st.session_state.translated_text = ''
        # Reset the target language to default
        st.session_state.target_language = 'fr'
