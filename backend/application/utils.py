import requests
import pandas as pd
import os

def transliterate_sentence(sentence, source_script, target_script="ISO"):
    # Construct the API URL with the provided parameters
    api_url = f"http://aksharamukha-plugin.appspot.com/api/public?source={source_script}&target={target_script}&text={sentence}"
    
    # Send a GET request to the API
    response = requests.get(api_url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract and return the transliterated text from the response
        return response.text
    else:
        # If the request was not successful, return None
        return None

lang_dict = {
    'hin': 'Hindi',
    'asm': 'Assamese',
    'ben': 'Bengali',
    'brx': 'Bodo',
    'doi': 'Dogri',
    'guj': 'Gujarati',
    'kan': 'Kannada',
    'kas': 'Kashmiri',
    'kok': 'Konkani',
    'mai': 'Maithili',
    'mal': 'Malayalam',
    'mar': 'Marathi',
    'mni': 'Manipuri',
    'nep': 'Nepali',
    'ori': 'Odia',
    'pan': 'Punjabi',
    'san': 'Sanskrit',
    'sat': 'Santali',
    'snd': 'Sindhi',
    'tam': 'Tamil',
    'tel': 'Telugu',
    'urd': 'Urdu'
}

ak = {
    "guj": ["Gujarati", ""],
    "hin": ["Devanagari", "RemoveSchwaHindi"],
    "kan": ["Kannada", ""],
    "mal": ["Malayalam", ""],
    "mar": ["Devanagari", "AnusvaratoNasalASTISO"],
    "pan": ["Gurmukhi", ""],
    "tam": ["Tamil", ""],
    "urd": ["Urdu", ""],
    "brx": ["Devanagari", ""],
    "ben": ["Bengali", ""],
    "mni": ["MeeteiMayek", ""],
    "nep": ["Newa", ""],
    "kok": ["Devanagari", ""],
    "ori": ["Oriya", ""],
    "san": ["Devanagari", ""],
    "snd": ["Devanagari", ""],
    "tel": ["Telugu", ""],
    "sat": ["Santali", ""],
    "asm": ["Assamese", ""],
    "doi": ["Devanagari", ""],
    "kas": ["Arab", ""],
    "mai": ["Tirhuta", ""],
}

emo2id = [
    'NEUTRAL',
    'HAPPY',
    'SAD',
    'ANGER',
    'FEAR',
    'SURPRISE',
    'DISGUST',
    'ALEXA',
    'DIGI',
    'BOOK',
    'CONV',
    'NEWS',
    'PROPER NOUN',
    'UMANG',
    'BB',
]