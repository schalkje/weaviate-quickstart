import os
from typing import List
import requests
import weaviate
import weaviate.classes as wvc
import json

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

    # if the collecttion does not exist, exit with a notification
    if collection_name not in client.collections.list_all(True):
        print(f"Collection '{collection_name}' does not exist")
        exit()

    chunks = client.collections.get(collection_name)

    # # Single query
    # response = chunks.generate.fetch_objects(
    #     limit=2, single_prompt="Write the following as a haiku: ===== {chunk} "
    # )

    # for o in response.objects:
    #     print(f"\n===== Object index: [{o.properties['chunk_index']}] =====")
    #     print(o.generated)

    # # grouped tasks
    # response = chunks.generate.fetch_objects(
    #     limit=2,
    #     grouped_task="Write a trivia tweet based on this text. Use emojis and make it succinct and cute.",
    # )

    # print(response.generated)

    # Pairing with search
    response = chunks.generate.near_text(
        query="states of git",
        limit=2,
        grouped_task="Write a trivia tweet based on this text. Use emojis and make it succinct and cute.",
    )

    print(response.generated)


finally:
    client.close()  # Close client gracefully
