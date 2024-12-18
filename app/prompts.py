import pandas as pd
import chromadb
import uuid
from langchain_community.document_loaders.csv_loader import CSVLoader

class Prompts:
    def __init__(self, file_path = "app/resources/train.csv"):
        self.file_path = file_path
        loader = CSVLoader(file_path)
        self.data = data = loader.load()
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
        self.chroma_client = chromadb.PersistentClient('chromadb')
        self.collection = self.chroma_client.get_or_create_collection(name="queries")
        print("Collection loaded successfully")

    def load_prompts(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["context"]],
                    metadatas=[{"responses": row["response"]}],
                    ids=[str(uuid.uuid4())]
                )
        print("Prompts loaded successfully")

    def query_responses(self, question):
        print("Querying responses")
        return self.collection.query(query_texts=[question],n_results=5).get('metadatas',[])