# List class
class MyList(list):
     pass

# Model class
class Model(str):
     pass

# Template function that takes a string and two objects as input and returns a list
def shopTemplate(prompt:str, plugin, context):
     my_list = MyList
     my_list = [
          {"role": "system", "content": plugin},
          {"role": "user", "content": f'Using this data {context}, respond to this prompt {prompt}.'},
          ]
     return my_list

def chatTemplate(prompt:str, plugin):
     my_list = MyList
     my_list = [
          {"role": "system", "content": plugin},
          {"role": "user", "content": f'{prompt}.'},
          ]
     return my_list

# Model function that returns the model as a string
def model():
     model = Model("C:\\Users\\RackUnit-1\\Models\\MetaAI\\meta-llama-3.1-8b-instruct-q4_k_m.gguf")
     return model
