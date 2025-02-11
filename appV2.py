import streamlit as st
import json
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
import pandas as pd
import time

def loadJSon():
    with st.spinner("Processing..."):
        #with open("entities_dummy_data.json", encoding="utf-8") as fd:
        with open("lastData.txt", 'r') as file:
            file_contents = file.read()
             #file_contents = pd.read_json(fd).to_csv(index=False)
        return file_contents

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", 
        chunk_size=1000, 
        chunk_overlap=200, 
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(model="gpt-4o")
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=vectorstore.as_retriever(), 
        memory=memory
    )
    return conversation_chain

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with SYNAPSE", layout="wide")
    st.image("https://i.ibb.co/2qVBw80/cc-2.png",width=200)

    st.write(css, unsafe_allow_html=True)

    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None



    # Display chat history at the top
    st.header("Chat with SYNAPSE")
    
    # Check if chat history exists and display messages
    if st.session_state.chat_history:
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
    else:
        if st.button("Start a conversation with Synapse !"):
         with st.spinner("Processing"):
              
                raw_text = loadJSon()
                # get the text chunks
                text_chunks = get_text_chunks(raw_text)
                # create vector store
                vectorstore = get_vectorstore(text_chunks)
                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)

    # Chat input at the bottom
    if st.session_state.conversation:
        user_question = st.chat_input("Ask a question to SYNAPSE")
        
        if user_question:
            # Handle user input 
                st.text('Fetching response...')
                st.image("https://s7.gifyu.com/images/SJZcn.gif",width=50)
                response = st.session_state.conversation({'question': user_question})
                st.session_state.chat_history = response['chat_history']
                time.sleep(2)
                
                # Rerun to refresh the page and show new messages
                st.rerun()

if __name__ == '__main__':
    main()