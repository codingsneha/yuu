from dotenv import load_dotenv
from PIL import Image
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get repsonses
model=genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

image = Image.open('yuu.png')

def get_gemini_response(question):
    response=chat.send_message(question,stream=True)
    return response

##initialize our streamlit app
st.set_page_config(page_title="Yuu")
st.image(image, width=200)
st.header("Chat with Yuu")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


input=st.text_input("Input: ",key="input")
output=""
history=""

submit=st.button("Send")

if submit and input:
    for role, text in st.session_state['chat_history']:
        history+=f"{role}: {text}"
    response=get_gemini_response("Context: You have to act as a cute therapist chatting friend who's name is 'Yuu' and respond to the user maybe taking into account the chat history, User: "+input+" Here's the past chat history just for context: "+history)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        output+=chunk.text
    st.session_state['chat_history'].append(("Yuu", output))
st.subheader("Chat History:")
    
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")