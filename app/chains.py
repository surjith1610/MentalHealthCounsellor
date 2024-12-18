import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(groq_api_key = os.getenv('GROQ_API_KEY'), model_name = "llama-3.3-70b-versatile", temperature=0)
        print("Model loaded successfully")

    def response_generator(self, question, responses):
        prompt_response = PromptTemplate.from_template(
        """
        ### This is a data from mental health counselling dataset
        {responses}
        ### Instruction:
        You are a mental health therapist
        This data represents a collection of mental health counselling records, including both the context (question) and the response.
        Use this data context and response to provide a summary answer to the question asked.
        Keep the answer short
        If the question is irrelevant just tell it's an irrelevant context
        ### Question:
        {question}
        ### Response:
        """
    )

        #Chain Extract
        chain_extract = prompt_response | self.llm

        res = chain_extract.invoke(input={"responses": responses, "question": question})

        print("Inside response generator")

        return res.content