import json

from langchain_core.tools import tool
from opensearch_client import opensearch_vector_store


@tool
def search(query: str):
    """Perform a semantic search of Northwestern University Library digital collections. When answering a search query, ground your answer in the context of the results with references to the document's metadata."""
    query_results = opensearch_vector_store.similarity_search(query, size=20)
    return json.dumps(query_results, default=str)

@tool
def aggregate(aggregation_query: str):
    """Perform a quantitative aggregation on the OpenSearch index.

    Available fields:
        ['accession_number', 'api_link', 'api_model', 'ark', 'box_name', 'box_number', 'catalog_key', 'collection.title.keyword', 'contributor.label.keyword', 'create_date', 'creator.id', 'date_created', 'embedding_model', 'embedding_text_length', 'genre.id', 'id', 'indexed_at', 'language.id', 'legacy_identifier', 'library_unit', 'license.id', 'location.id', 'modified_date', 'preservation_level', 'provenance', 'published', 'publisher', 'related_url.label', 'rights_holder', 'rights_statement.id', 'scope_and_contents', 'series', 'source', 'status', 'style_period.label.keyword', 'style_period.variants', 'subject.id', 'subject.variants', 'table_of_contents', 'technique.id', 'technique.variants', 'terms_of_use', 'title.keyword', 'visibility', 'work_type']

    Examples:
    Query about the number of collections: collection.title.keyword
    Query about the number of works by work type: work_type
    """
    try:
        response = opensearch_vector_store.aggregations_search(aggregation_query)
        return json.dumps(response, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})