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
    # check if there are already collections in the Weaviate instance, if yes, disply them
    collections = client.collections.list_all(True)
    if len(collections) > 0:
        print("Collections in Weaviate instance:")
        for collection in collections:
            print("- " + collection)
    else:
        print("No collections in Weaviate instance")

    # remove the collection "Question" if it already exists
    # if "Question" in client.collections.list_all(True):
    #     client.collections.delete("Question")
    #     print("Collection 'Question' deleted")
    # else:
    #     print("Collection 'Question' does not exist")

    # validate if the collection exists, if not, create it
    if "Question" not in client.collections.list_all(True):
        questions = client.collections.create(
            name="Question",
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
            generative_config=wvc.config.Configure.Generative.openai(),  # Ensure the `generative-openai` module is used for generative queries
        )

        resp = requests.get(
            "https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json"
        )
        data = json.loads(resp.text)  # Load data

        question_objs = list()
        for i, d in enumerate(data):
            question_objs.append(
                {
                    "answer": d["Answer"],
                    "question": d["Question"],
                    "category": d["Category"],
                }
            )

        questions = client.collections.get("Question")
        questions.data.insert_many(question_objs)  # This uses batching under the hood

        print("Collection created and data loaded")
    else:
        print("Collection already exists")

    # validate if the data is already loaded by printing the first 5 objects
    questions = client.collections.get("Question")
    response = questions.query.fetch_objects(limit=30)
    for obj in response.objects:
        print(obj.properties)


finally:
    client.close()  # Close client gracefully
