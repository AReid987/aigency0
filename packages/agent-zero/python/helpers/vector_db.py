import json
import os
import uuid

import faiss
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import InMemoryByteStore, LocalFileStore
from langchain_chroma import Chroma
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from python.helpers import knowledge_import
from python.helpers.log import Log

from . import files

<< << << < HEAD


class VectorDB:

    def __init__(self, embeddings_model, in_memory=False, cache_dir="./cache"):
        print("Initializing VectorDB...")
        self.embeddings_model = embeddings_model

        em_cache = files.get_abs_path(cache_dir, "embeddings")
        db_cache = files.get_abs_path(cache_dir, "database")


== == == =


# from langchain_chroma import Chroma


class VectorDB:

    def __init__(self, logger: Log, embeddings_model, in_memory=False, memory_dir="./memory", knowledge_dir="./knowledge"):
        self.logger = logger

        print("Initializing VectorDB...")
        self.logger.log("info", content="Initializing VectorDB...")

        self.embeddings_model = embeddings_model

        self.em_dir = files.get_abs_path(memory_dir, "embeddings")
        self.db_dir = files.get_abs_path(memory_dir, "database")
        self.kn_dir = files.get_abs_path(
            knowledge_dir) if knowledge_dir else ""


>>>>>> > 83f71b59(new remote. who dis?)

        if in_memory:
            self.store = InMemoryByteStore()
        else:
<< << << < HEAD
            self.store = LocalFileStore(em_cache)
== == == =
            self.store = LocalFileStore(self.em_dir)
>>>>>> > 83f71b59(new remote. who dis?)

        # here we setup the embeddings model with the chosen cache storage
        self.embedder = CacheBackedEmbeddings.from_bytes_store(
            embeddings_model,
            self.store,
            namespace=getattr(embeddings_model, 'model', getattr(embeddings_model, 'model_name', "default")))

<< << << < HEAD

        self.db = Chroma(embedding_function=self.embedder,
                         persist_directory=db_cache)

== == == =
        # self.db = Chroma(
        #     embedding_function=self.embedder,
        #     persist_directory=db_dir)

        # if db folder exists and is not empty:
        if os.path.exists(self.db_dir) and files.exists(self.db_dir, "index.faiss"):
            self.db = FAISS.load_local(
                folder_path=self.db_dir,
                embeddings=self.embedder,
                allow_dangerous_deserialization=True
            )
        else:
            index = faiss.IndexFlatL2(
                len(self.embedder.embed_query("example text")))

            self.db = FAISS(
                embedding_function=self.embedder,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={})

        # preload knowledge files
        if self.kn_dir:
            self.preload_knowledge(self.kn_dir, self.db_dir)


    def preload_knowledge(self, kn_dir:str, db_dir:str):

        # Load the index file if it exists
        index_path = files.get_abs_path(db_dir, "knowledge_import.json")

        #make sure directory exists
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        index: dict[str, knowledge_import.KnowledgeImport] = {}
        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                index = json.load(f)
       
        index = knowledge_import.load_knowledge(self.logger,kn_dir,index)
        
        for file in index:
            if index[file]['state'] in ['changed', 'removed'] and index[file].get('ids',[]): # for knowledge files that have been changed or removed and have IDs
                self.delete_documents_by_ids(index[file]['ids']) # remove original version
            if index[file]['state'] == 'changed':
                index[file]['ids'] = self.insert_documents(index[file]['documents']) # insert new version

        # remove index where state="removed"
        index = {k: v for k, v in index.items() if v['state'] != 'removed'}
        
        # strip state and documents from index and save it
        for file in index:
            if "documents" in index[file]: del index[file]['documents'] # type: ignore
            if "state" in index[file]: del index[file]['state'] # type: ignore
        with open(index_path, 'w') as f:
            json.dump(index, f)    
>>>>>>> 83f71b59 (new remote. who dis?)
        
    def search_similarity(self, query, results=3):
        return self.db.similarity_search(query,results)
    
    def search_similarity_threshold(self, query, results=3, threshold=0.5):
        return self.db.search(query, search_type="similarity_score_threshold", k=results, score_threshold=threshold)

    def search_max_rel(self, query, results=3):
        return self.db.max_marginal_relevance_search(query,results)

    def delete_documents_by_query(self, query:str, threshold=0.1):
        k = 100
        tot = 0
        while True:
            # Perform similarity search with score
            docs = self.search_similarity_threshold(query, results=k, threshold=threshold)

            # Extract document IDs and filter based on score
            # document_ids = [result[0].metadata["id"] for result in docs if result[1] < score_limit]
            document_ids = [result.metadata["id"] for result in docs]
            

            # Delete documents with IDs over the threshold score
            if document_ids:
                # fnd = self.db.get(where={"id": {"$in": document_ids}})
                # if fnd["ids"]: self.db.delete(ids=fnd["ids"])
                # tot += len(fnd["ids"])
                self.db.delete(ids=document_ids)
                tot += len(document_ids)
                                    
            # If fewer than K document IDs, break the loop
            if len(document_ids) < k:
                break
<<<<<<< HEAD
        
=======

        if tot: self.db.save_local(folder_path=self.db_dir) # persist
>>>>>>> 83f71b59 (new remote. who dis?)
        return tot

    def delete_documents_by_ids(self, ids:list[str]):
        # pre = self.db.get(ids=ids)["ids"]
        self.db.delete(ids=ids)
        # post = self.db.get(ids=ids)["ids"]
        #TODO? compare pre and post
<<<<<<< HEAD
        return len(ids)
        
    def insert_document(self, data):
        id = str(uuid.uuid4())
        self.db.add_documents(documents=[ Document(data, metadata={"id": id}) ], ids=[id])
        
        return id
        
=======
        if ids: self.db.save_local(folder_path=self.db_dir) #persist
        return len(ids)
        
    def insert_text(self, text):
        id = str(uuid.uuid4())
        self.db.add_documents(documents=[ Document(text, metadata={"id": id}) ], ids=[id])
        self.db.save_local(folder_path=self.db_dir) #persist
        return id
    
    def insert_documents(self, docs:list[Document]):
        ids = [str(uuid.uuid4()) for _ in range(len(docs))]
        for doc, id in zip(docs, ids): doc.metadata["id"] = id  #add ids to documents metadata
        self.db.add_documents(documents=docs, ids=ids)
        self.db.save_local(folder_path=self.db_dir) #persist
        return ids
>>>>>>> 83f71b59 (new remote. who dis?)


