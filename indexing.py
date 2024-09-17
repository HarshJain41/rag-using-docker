# indexing.py
from pinecone import Pinecone, ServerlessSpec
import time

# Initialize Pinecone and create unique index
def initialize_pinecone(pinecone_api_key, index_name):

    spec = ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )

    pinecone_api = pinecone_api_key
    pc = Pinecone(api_key=pinecone_api)

    existing_indexes = [
    index_info["name"] for index_info in pc.list_indexes()]

    # check if index already exists (it shouldn't if this is first time)
    if index_name not in existing_indexes:
        # if does not exist, create index
        pc.create_index(
            index_name,
            dimension=4096,  # dimensionality of ada 002
            metric='dotproduct',
            spec=spec
        )
        # wait for index to be initialized
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)

    # connect to index
    index = pc.Index(index_name)
    time.sleep(1)

    return index

# Delete Pinecone index when user quits
def delete_index(index_name, pinecone_api_key):
    pc = Pinecone(api_key=pinecone_api_key) 
    pc.delete_index(index_name)
