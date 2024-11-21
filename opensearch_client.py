import os
import boto3

from dotenv import load_dotenv
from opensearch_neural_search import OpenSearchNeuralSearch
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from urllib.parse import urlparse

load_dotenv()


def prefix(value):
    env_prefix = os.getenv("ENV_PREFIX")
    env_prefix = None if env_prefix == "" else env_prefix
    return "-".join(filter(None, [env_prefix, value]))


def opensearch_endpoint():
    endpoint = os.getenv("OPENSEARCH_ENDPOINT")
    parsed = urlparse(endpoint)
    if parsed.netloc != "":
        return parsed.netloc
    else:
        return endpoint


def opensearch_client(region_name=os.getenv("AWS_REGION", "us-east-1")):
    session = boto3.Session(region_name=region_name)
    print(f"Session: {session}")

    awsauth = AWS4Auth(
        region=region_name,
        service="es",
        refreshable_credentials=session.get_credentials(),
    )

    return OpenSearch(
        hosts=[{"host": opensearch_endpoint(), "port": 443}],
        use_ssl=True,
        connection_class=RequestsHttpConnection,
        http_auth=awsauth,
    )


def opensearch_vector_store(
    index="dc-v2-work", region_name=os.getenv("AWS_REGION", "us-east-1")
):
    session = boto3.Session(region_name=region_name)
    awsauth = AWS4Auth(
        region=region_name,
        service="es",
        refreshable_credentials=session.get_credentials(),
    )

    docsearch = OpenSearchNeuralSearch(
        index=prefix(index),
        model_id=os.getenv("OPENSEARCH_MODEL_ID"),
        endpoint=opensearch_endpoint(),
        connection_class=RequestsHttpConnection,
        http_auth=awsauth,
        text_field="id",
    )
    return docsearch


# Define the OpenSearch cluster connection
opensearch_client = opensearch_client()

# Retrieve cluster information
info = opensearch_client.info()
print(f"Connected to OpenSearch version {info['version']['number']}")


opensearch_vector_store = opensearch_vector_store()



