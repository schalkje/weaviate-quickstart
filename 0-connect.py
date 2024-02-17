import os
import weaviate
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
    response = client.get_meta()
    print(response)

    pass  # Add an indented block of code here if needed

finally:
    client.close()  # Close client gracefully
