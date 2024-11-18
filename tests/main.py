from opensearch_client import opensearch_vector_store

def test_aggregations_search():
    # Terms Aggregation on `genre.label` with Sub-Aggregation on `style_period.label`
    aggregations_genres = {
        "genres": {
            "terms": {
                "field": "genre.label",
                "size": 10
            },
            "aggs": {
                "style_periods": {
                    "terms": {
                        "field": "style_period.label",
                        "size": 5
                    }
                }
            }
        }
    }
    
    try:
        results_genres = opensearch_vector_store.aggregations_search(aggregations_genres)
        print("Genres with Style Periods Aggregation Results:", results_genres)
    except Exception as e:
        print(f"An error occurred in Genres Aggregation: {e}")
    
    # Date Histogram Aggregation on `create_date`
    aggregations_creation_dates = {
        "creation_dates": {
            "date_histogram": {
                "field": "create_date",
                "calendar_interval": "month",
                "format": "yyyy-MM"
            }
        }
    }
    
    try:
        results_creation_dates = opensearch_vector_store.aggregations_search(aggregations_creation_dates)
        print("Creation Dates Aggregation Results:", results_creation_dates)
    except Exception as e:
        print(f"An error occurred in Creation Dates Aggregation: {e}")
    
    # Cardinality Aggregation on `creator.id`
    aggregations_unique_creators = {
        "unique_creators": {
            "cardinality": {
                "field": "creator.id"
            }
        }
    }
    
    try:
        results_unique_creators = opensearch_vector_store.aggregations_search(aggregations_unique_creators)
        print("Unique Creators Aggregation Results:", results_unique_creators)
    except Exception as e:
        print(f"An error occurred in Unique Creators Aggregation: {e}")
    
    # Average Calculation on `embedding_text_length`
    aggregations_average_embedding = {
        "average_embedding_length": {
            "avg": {
                "field": "embedding_text_length"
            }
        }
    }
    
    try:
        results_average_embedding = opensearch_vector_store.aggregations_search(aggregations_average_embedding)
        print("Average Embedding Length Aggregation Results:", results_average_embedding)
    except Exception as e:
        print(f"An error occurred in Average Embedding Length Aggregation: {e}")
    
    # Top Hits Aggregation to Retrieve Sample Documents per Genre
    aggregations_genres_top_works = {
        "genres_top_works": {
            "terms": {
                "field": "genre.label",
                "size": 10
            },
            "aggs": {
                "top_works": {
                    "top_hits": {
                        "size": 3,
                        "_source": ["title", "creator.label", "create_date"]
                    }
                }
            }
        }
    }
    
    try:
        results_genres_top_works = opensearch_vector_store.aggregations_search(aggregations_genres_top_works)
        print("Genres Top Works Aggregation Results:", results_genres_top_works)
    except Exception as e:
        print(f"An error occurred in Genres Top Works Aggregation: {e}")
    
    # Range Aggregation on `embedding_text_length`
    aggregations_embedding_length_ranges = {
        "embedding_length_ranges": {
            "range": {
                "field": "embedding_text_length",
                "ranges": [
                    {"to": 500},
                    {"from": 500, "to": 1000},
                    {"from": 1000}
                ]
            }
        }
    }
    
    try:
        results_embedding_length_ranges = opensearch_vector_store.aggregations_search(aggregations_embedding_length_ranges)
        print("Embedding Length Ranges Aggregation Results:", results_embedding_length_ranges)
    except Exception as e:
        print(f"An error occurred in Embedding Length Ranges Aggregation: {e}")

if __name__ == "__main__":
    test_aggregations_search() 