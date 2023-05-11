import argparse
import json
from dotenv import load_dotenv
import os
import weaviate
from data_loader import load_dataset

load_dotenv()

parser = argparse.ArgumentParser()
# Pass --load to load the dataset into the cluster
parser.add_argument("--load", action="store_true")
# Pass --neartext to run the nearText query
parser.add_argument("--neartext", action="store_true")
# Pass --nearvector to run the nearVector query
parser.add_argument("--nearvector", action="store_true")

args = parser.parse_args()

weaviate_cluster_url = os.getenv("WEAVIATE_CLUSTER_URL", "")
weaviate_api_key = os.getenv("WEAVIATE_API_KEY", "")
openai_api_key = os.getenv("OPENAI_API_KEY", "")

client = weaviate.Client(
    url=weaviate_cluster_url,
    auth_client_secret=weaviate.auth.AuthApiKey(api_key=weaviate_api_key),
    additional_headers={"X-OpenAI-Api-Key": openai_api_key},
)

result = ""

# See https://weaviate.io/developers/weaviate/quickstart/end-to-end#load--import-data for more info
if args.load:
    print("Creating schema ...")
    class_obj = {
        "class": "Question",
        "vectorizer": "text2vec-openai",
    }
    client.schema.create_class(class_obj)
    print("Loading dataset into cluster ...")
    load_dataset(client)

# See https://weaviate.io/developers/weaviate/tutorials/query#get-with-neartext for more info
if args.neartext:
    nearText = {"concepts": ["mammals"]}

    result = (
        client.query.get("Question", ["question", "answer", "category"])
        .with_near_text(nearText)
        .with_limit(2)
        .do()
    )

# See https://weaviate.io/developers/weaviate/tutorials/query#get-with-nearvector for more info
if args.nearvector:
    import openai

    openai.api_key = openai_api_key
    model = "text-embedding-ada-002"
    oai_resp = openai.Embedding.create(input=["biology"], model=model)
    oai_emedding = oai_resp["data"][0]["embedding"]

    result = (
        client.query.get(
            "Question",
            [
                "question",
                "answer",
            ],
        )
        .with_near_vector({"vector": oai_emedding, "certainty": 0.7})
        .with_limit(2)
        .do()
    )

print(json.dumps(result, indent=4))
