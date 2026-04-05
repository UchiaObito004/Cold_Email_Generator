# portfolio.py
import uuid
import pandas as pd
import chromadb

class Portfolio:
    def __init__(self, file_path: str = "my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient("vectorstore")
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self, force_reload: bool = False) -> None:
        if force_reload and self.collection.count() > 0:
            existing_ids = self.collection.get()["ids"]
            if existing_ids:
                self.collection.delete(ids=existing_ids)

        if self.collection.count() == 0:
            documents, metadatas, ids = [], [], []
            for _, row in self.data.iterrows():
                techstack = str(row.get("Techstack", "")).strip()
                link = str(row.get("Links", "")).strip()
                if techstack and link:              # skip empty rows
                    documents.append(techstack)
                    metadatas.append({"links": link})
                    ids.append(str(uuid.uuid4()))

            if documents:
                self.collection.add(documents=documents, metadatas=metadatas, ids=ids)

    def query_links(self, skills: list, n_results: int = 2) -> list:
        if not skills:
            return []
        n_results = min(n_results, self.collection.count())  # fix crash
        if n_results == 0:
            return []
        return self.collection.query(query_texts=skills, n_results=n_results).get("metadatas", [])
