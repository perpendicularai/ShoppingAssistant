from SeKernel_for_LLM import kernel
from SeKernel_for_LLM import plugins
from llama_cpp import Llama
from pprint import pp
import pyttsx3
import os
import sys

# Initialize Speech-engine
engine = pyttsx3.init()

# Initialize LlamaCpp
llm = Llama(
            model_path=kernel.model(),
            # Models may be downloaded from Huggingface. See - https://huggingface.co/models?pipeline_tag=text-generation&sort=trending&search=gguf
            n_ctx=4098, # Token context amount
            )
# Speech-engine call for app intro
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) # setProperty method
engine.say("Please provide a topic to shop or search for. It can be anything that is advertised online. Or type exit to quit.")
engine.runAndWait()
engine.stop()

# Input for topic
question = input("Please provide a shopping topic or type (exit) to quit: ")
if question == "exit":
      sys.exit()
elif question != "exit":
    try:
         # Internet-search plugin bundled with the shopping template. See SeKernel_for_LLM directory for more.
         search_prompt = plugins.searchPlugin(output=question)
         data = kernel.shopTemplate(prompt=question, plugin=plugins.shopPlugin(), context=search_prompt)
         
         # Generate response using output data from the internet crawl parsed to the llm:
         output = llm.create_chat_completion(
              messages=data
              )
         
         response = {"role":"assistant", "content":""}
         response['content'] += output['choices'][0]['message']['content']
         
         # Chat template bundled with the shopping plugin. See SeKernel_for_LLM directory for more.
         data2 = kernel.chatTemplate(
              prompt=question,
              plugin=plugins.shopPlugin(),
              )
         data2.append(response)

         # Speech-engine call for gathered information alert
         voices = engine.getProperty('voices')
         engine.setProperty('voice', voices[1].id) # setProperty method
         engine.say("The information on your shopping topic has been gathered and you may now start your conversation.")
         engine.runAndWait()
         engine.stop()
         print("The information on your shopping topic has been gathered and you may now start your conversation. If you would like to exit, press the control key + c.")
         print("\n")
         
         while True:
             try:
                 # Speech-engine call for notifying user to start conversation.
                 voices = engine.getProperty('voices')
                 engine.setProperty('voice', voices[1].id) # setProperty method
                 engine.say("You may start typing. If you would like to exit, press the control key + c.")
                 engine.runAndWait()
                 engine.stop()

                 # User input
                 data2.append({"role":"assistant", "content": input("> ")})

                 # Generate response based on the llm's awareness of the conversation, given the history parsed from the output of the previous llm call.
                 output2 = llm.create_chat_completion(
                     messages=data2
                     )
                 response2 = {"role":"assistant", "content": ""}
                 response2['content'] += output2['choices'][0]['message']['content']
                 response3 = output2['choices'][0]['message']['content']
                 data2.append(response2)
             
                 # Text-to-Speech engine used to vocally output the response (1-Female, 2-Male). See setProperty method:
                 voices = engine.getProperty('voices')
                 engine.setProperty('voice', voices[1].id) # setProperty method
                 engine.say(response3)
                 engine.runAndWait()
                 engine.stop()
             except KeyboardInterrupt:
                 voices = engine.getProperty('voices')
                 engine.setProperty('voice', voices[1].id) # setProperty method
                 engine.say("The program is now exiting. Goodbye!")
                 engine.runAndWait()
                 engine.stop()
                 sys.exit()
    except Exception as e:
        # Text-to-Speech engine used to vocally output the response (1-Female, 2-Male). See setProperty method:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id) # setProperty method
        engine.say("Check your internet connection.")
        engine.runAndWait()
        engine.stop()
