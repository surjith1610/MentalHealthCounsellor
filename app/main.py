from chains import Chain
from prompts import Prompts
from utils import clean_text
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader


def create_streamlit_app(llm, prompts, clean_text):
    st.title("Llama Mental Health Counsellor")
    input_text = st.text_area("Enter your question here")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            question = clean_text(input_text)
            prompts.load_prompts()
            responses = prompts.query_responses(question)
            result = chain.response_generator(question, responses)
            st.write(result)
        except Exception as e:
            st.write("Error in processing the question",e)

if __name__ == "__main__":
    chain = Chain()
    prompts = Prompts()
    st.set_page_config(page_title="Llama Mental Health Counsellor")
    create_streamlit_app(chain, prompts, clean_text)