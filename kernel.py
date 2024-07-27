# List class
class MyList(list):
     pass

# Model class
class Model(str):
     pass

# Template function that takes a string and two objects as input and returns a list
def template(prompt:str, plugin, context):
     my_list = MyList
     my_list = [
          {"role": "system", "content": plugin},
          {"role": "user", "content": f'Using this data {context}, respond to this prompt {prompt}'},
          ]
     return my_list

# Model function that returns the model as a string
def model():
     model = Model("<PATH TO GGUF MODEL>")
     return model
