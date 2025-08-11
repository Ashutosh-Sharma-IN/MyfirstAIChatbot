import streamlit as st
from streamlit_chat import message
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Initialize session state variables
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# ===================================================================
# CHOOSE YOUR MODEL: Uncomment only ONE of the blocks below
# ===================================================================

# --- BLOCK 1: Together.xyz (Llama) ---
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(
 #   model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
  #  openai_api_key=st.secrets["TOGETHER_API_KEY"],
   # openai_api_base="https://api.together.xyz/v1"


"""
# --- BLOCK 2: OpenAI (GPT) ---
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    openai_api_key=st.secrets["OPENAI_API_KEY"]
)
"""

"""
# --- BLOCK 3: Google (Gemini) ---
# from langchain_google_genai import ChatGoogleGenerativeAI
#llm = ChatGoogleGenerativeAI(
 #   model="gemini-pro",
  #  google_api_key=st.secrets["GOOGLE_API_KEY"]
#)
"""

# ===================================================================
# This part of the code stays the same no matter which block is active
# ===================================================================
conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

# Create user interface
st.title("🗣️ Conversational Chatbot")
st.subheader("㈻ Simple Chat Interface for LLMs by Build Fast with AI")


if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = conversation.predict(input = prompt)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # Add response to message history
