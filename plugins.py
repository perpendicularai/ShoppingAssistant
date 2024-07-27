# Plugin class
class Plugin(str):
     pass

## Plugins ##

# Default plugin
def defaultPlugin():
     system = Plugin(
          """
          You are an intelligent assistant. 
          You always provide well-reasoned answers that are both correct and helpful.
          """
          )
     return system

# Math plugin
def mathPlugin():
     system = Plugin(
          """
          You are an intelligent assistant proficient at Maths. 
          You always provide well-reasoned answers that are both correct and helpful.
          """
          )
     return system

# Internet-search plugin

# Module imports
from bs4 import BeautifulSoup
import requests

def searchPlugin(output):
    url = "https://google.com/search?q="+remove_pos_tags(output)
    # Fetch the URL data using requests.get(url), 
    # store it in a variable, request_result. 
    request_result=requests.get( url ) 
  
    # Creating soup from the fetched request 
    soup = BeautifulSoup(request_result.text, 
                         "html.parser")
    data = soup.get_text()
    return data

## Linguistic functions ##

# Module imports
from pathlib import Path
import nltk
import os

# Get env user
username = os.getenv("USERNAME")

# Specify the path to your local NLTK data directory
nltk_data_dir = Path(f"C:\\Users\\{username}\\data")

# Load NLTK data from the local directory
nltk.data.path.append(str(nltk_data_dir))

# Function to remove pos tagged words from the question
def remove_pos_tags(prompt):
    tokens = nltk.word_tokenize(prompt)
    tagged_tokens = nltk.pos_tag(tokens)
    return " ".join(token for token, pos in tagged_tokens if pos not in ['IN', 'TO', 'PRP', 'PRP$', 'VBZ', 'WRB', 'WP', 'DT', 'VB'])
