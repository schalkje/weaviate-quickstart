import os
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
    questions = client.collections.get("Question")

    response = questions.query.near_text(
        query="biology",
        limit=2,
        filters=wvc.query.Filter.by_property("category").equal("ANIMALS"),
    )

    # loop over all objects in the response
    for obj in response.objects:
        print(obj.properties)

finally:
    client.close()  # Close client gracefully
