from duckduckgo_search import DDGS
from llama_cpp import Llama
from pprint import pp
import pyttsx3
import os

username = os.getenv("USERNAME")
engine = pyttsx3.init()

# Strings to replace in response:
a="'"
b="*"
c="()"

# Start search
while True:
    prompt = input("Enter a search phrase: ")
    site_prompt = input("Select a supermarket to search: (1-Checkers, 2-PNP, 3-Woolworths) ")
    if site_prompt == "1":
        res = DDGS().text(f'{prompt} site:checkers.co.za')
    elif site_prompt == "2":
        res = DDGS().text(f'{prompt} site:pnp.co.za')
    elif site_prompt == "3":
        res = DDGS().text(f'{prompt} site:woolworths.co.za')
    
    # Response
    final_res = res[0]['body']

    llm = Llama(
        model_path=f"<PATH TO GGUF MODEL>",
        # Models may be downloaded from Huggingface. See - https://huggingface.co/models?pipeline_tag=text-generation&sort=trending&search=gguf
        n_ctx=4098,
    )

    # Generate response using output data parsed to the llm:
    output = llm.create_chat_completion(
        messages=[
            {
                'role':'system', 'content':'You are an AI shopping assistant. When formulating a list of items with prices always ensure that the prices are in South African Rand with the symbol R. Never formulate a list with items that are not in the provided data.',
                'role':'user', 'content':f'Using this data {final_res}, formulate a list of items with their prices in descending order.'
            }
        ]
    )
    
    response = output['choices'][0]['message']['content'].replace(a+b+c, " ")
    pp(response)

    # Text-to-Speech engine used to vocally output the response (1-Female, 2-Male). See setProperty method:
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) # setProperty method
    engine.say(response)
    engine.runAndWait()
    engine.stop()

    # Option to exit or continue:
    option = input("Type 'quit' to exit or 'continue': ")
    if option == "continue":
        continue
    elif option == 'quit':
        break
    elif option != 'quit' and option != 'continue':
        break