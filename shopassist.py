from SeKernel_for_LLM import kernel
from SeKernel_for_LLM import plugins
from llama_cpp import Llama
from pprint import pp
import pyttsx3
import os

username = os.getenv("USERNAME")
engine = pyttsx3.init()

question = input("Shop: ")
search_prompt = plugins.searchPlugin(output=question)
data = kernel.template(prompt=question, plugin=plugins.shopPlugin(), context=search_prompt)


llm = Llama(
    model_path=kernel.model(),
        # Models may be downloaded from Huggingface. See - https://huggingface.co/models?pipeline_tag=text-generation&sort=trending&search=gguf
    n_ctx=4098,
    )

# Generate response using output data parsed to the llm:
output = llm.create_chat_completion(
    messages=data
    )
    
response = output['choices'][0]['message']['content']
pp(response)

# Text-to-Speech engine used to vocally output the response (1-Female, 2-Male). See setProperty method:
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) # setProperty method
engine.say(response)
engine.runAndWait()
engine.stop()

while True:
    # Option to exit or continue:
    option = input("Type 'quit' to exit or 'continue': ")
    if option == "continue":
        continue
    elif option == 'quit':
        break
    elif option != 'quit' and option != 'continue':
        break