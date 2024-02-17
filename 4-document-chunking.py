import os
from typing import List
import requests
import weaviate
import weaviate.classes as wvc
import json


def download_and_chunk(src_url: str, chunk_size: int, overlap_size: int) -> List[str]:
    import requests
    import re

    response = requests.get(src_url)  # Retrieve source text
    source_text = re.sub(r"\s+", " ", response.text)  # Remove multiple whitespaces
    text_words = re.split(r"\s", source_text)  # Split text by single whitespace

    chunks = []
    for i in range(0, len(text_words), chunk_size):  # Iterate through & chunk data
        chunk = " ".join(
            text_words[max(i - overlap_size, 0) : i + chunk_size]
        )  # Join a set of words into a string
        chunks.append(chunk)
    return chunks


client = weaviate.connect_to_custom(
    http_host="localhost",
    http_port="8080",
    http_secure=False,
    grpc_host="localhost",
    grpc_port="50051",
    grpc_secure=False,
    headers={"X-OpenAI-Api-Key": os.environ["OPENAI_APIKEY"]},
)

try:
    collection_name = "GitBookChunk"

    if client.collections.exists(
        collection_name
    ):  # In case we've created this collection before
        client.collections.delete(
            collection_name
        )  # THIS WILL DELETE ALL DATA IN THE COLLECTION

    chunks = client.collections.create(
        name=collection_name,
        properties=[
            wvc.config.Property(name="chunk", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(
                name="chapter_title", data_type=wvc.config.DataType.TEXT
            ),
            wvc.config.Property(name="chunk_index", data_type=wvc.config.DataType.INT),
        ],
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),  # Use `text2vec-openai` as the vectorizer
        generative_config=wvc.config.Configure.Generative.openai(),  # Use `generative-openai` with default parameters
    )

    # Download and chunk the text
    pro_git_chapter_url = "https://raw.githubusercontent.com/progit/progit2/main/book/01-introduction/sections/what-is-git.asc"
    chunked_text = download_and_chunk(pro_git_chapter_url, 150, 25)

    # Insert the chunks into the collection
    chunks_list = list()
    for i, chunk in enumerate(chunked_text):
        data_properties = {
            "chapter_title": "What is Git",
            "chunk": chunk,
            "chunk_index": i,
        }
        data_object = wvc.data.DataObject(properties=data_properties)
        chunks_list.append(data_object)
    chunks.data.insert_many(chunks_list)

    # Aggregate over all chunks and count them
    response = chunks.aggregate.over_all(total_count=True)
    print(f"The chapter has {response.total_count} chunks")

finally:
    client.close()  # Close client gracefully
