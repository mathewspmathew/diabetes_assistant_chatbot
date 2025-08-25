import google.generativeai as genai
import os

# Configure the client with your API key
genai.configure(api_key="AIzaSyDhg-F-xHLo-55SR0Eh2KlS9TXDrOKMuLQ")

# List all available models and print their names
for model in genai.list_models():
    print(model.name)
