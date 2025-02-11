import os
import time
from flask import Flask, request, render_template
from dotenv import load_dotenv

# LangChain imports
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

load_dotenv()  # Load .env if you store OPENAI_API_KEY or other secrets

app = Flask(__name__)

# --------------------------
# Global variables for the demo:
# In production (especially on serverless), you might need
# external storage for chat_history or conversation_chain
# to ensure continuity across requests.
# --------------------------
conversation_chain = None
chat_history = []


def load_json():
    """
    Loads your file data. 
    Equivalent to your loadJSon() function in Streamlit code.
    """
    # In your case, you were loading from "lastData.txt"
    # or some other file. Adapt as needed:
    with open("lastData.txt", "r", encoding="utf-8") as f:
        file_contents = f.read()
    return file_contents


def get_text_chunks(text):
    """
    Splits text into chunks for embeddings.
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    """
    Builds a FAISS vectorstore from text chunks using OpenAI embeddings.
    """
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vectorstore


def create_conversation_chain(vectorstore):
    """
    Creates the ConversationalRetrievalChain using ChatOpenAI (GPT-4).
    """
    llm = ChatOpenAI(model="gpt-4")  # or whichever model you want
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main route to display and handle the chat.
    """
    global conversation_chain, chat_history

    # If GET request, it means user just opened the page
    if request.method == 'GET':
        # If we have not yet loaded or created our conversation chain, do it now:
        if conversation_chain is None:
            raw_text = load_json()
            text_chunks = get_text_chunks(raw_text)
            vectorstore = get_vectorstore(text_chunks)
            conversation_chain = create_conversation_chain(vectorstore)

        # Render the page with the current chat history
        # (which might be empty at first).
        return render_template('index.html', chat_history=chat_history)

    else:
        # POST request: user submitted a question from the form
        user_question = request.form.get('user_question', '')

        if user_question.strip():
            # Get a response from the chain
            response = conversation_chain({'question': user_question})
            chat_history = response['chat_history']

            # Optional: you can add a small delay to mimic "thinking" as in Streamlit
            time.sleep(1)

        # Re-render the page with the updated chat history
        return render_template('index.html', chat_history=chat_history)


if __name__ == '__main__':
    # For local development
    app.run(debug=True)
