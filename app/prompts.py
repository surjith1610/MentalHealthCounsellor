import pandas as pd
import chromadb
import uuid
from langchain_community.document_loaders.csv_loader import CSVLoader
import os
from langchain.embeddings import OpenAIEmbeddings

class Prompts:
    embedding = OpenAIEmbeddings(openai_api_key=os.getenv('OPEN_AI_API_KEY'), model='text-embedding-3-small')
    def __init__(self, file_path = "app/resources/train.csv"):
        self.file_path = file_path
        loader = CSVLoader(file_path)
        self.data = loader.load()
        #Iterate and store the output data in a sperate list as dictionaries
        self.output_data = []
        # Loop through each document in the loaded data
        for doc in self.data:
            # Get the page content (which contains both context and response)
            page_content = doc.page_content
            
            # Split the page content into context and response
            if "Response:" in page_content:
                context = page_content.split("Response:")[0].replace("Context:", "").strip()
                response = page_content.split("Response:")[1].strip()

                # Append the extracted context and response to the output_data list
                self.output_data.append({
                    "context": context,
                    "response": response
                })
            else:
                print("Response not found in page content.")

        self.data = pd.DataFrame(self.output_data)
        self.chroma_client = chromadb.PersistentClient('chromadbnewtest')
        self.collection = self.chroma_client.get_or_create_collection(name="queries")
        print("Collection loaded successfully")

    def load_prompts(self):
        
        if not self.collection.count():
            try:
                for _, row in self.data.iterrows():
                    # Generate embedding
                    context_embedding = self.embedding.embed_documents([row["context"]])[0]
                    self.collection.add(
                        documents=[row["context"]],
                        embeddings=[context_embedding],
                        metadatas=[{"response": row["response"]}],
                        ids=[str(uuid.uuid4())]
                    )
                    print(f"Row added: {row}")
            except Exception as e:
                print(f"Error adding row: {row}, Error: {e}")
        print("Prompts loaded successfully")

    def query_responses(self, question):
        try:
            # Generate embedding for the question
            question_embedding = self.embedding.embed_documents([question])[0]
            # print("Embedded question", question_embedding)
            print("Querying responses")
            results = self.collection.query(query_embeddings=[question_embedding],n_results=5)
            
            #convert it to a single string
            retrieved_response = "\n".join(
        [metadata["response"] for metadata_list in results["metadatas"] for metadata in metadata_list])
            print("Querying responses done")
            # print(retrieved_response)
            
            return retrieved_response
        except Exception as e:
            print(f"Error querying responses: {e}")
            return "Error querying responses"