from qdrant_client.http.models import Filter, FieldCondition, MatchValue, MatchAny

def create_search_filter(classification: str, week_start=None):

    if not classification or classification.strip() == "":
        classification = "personal"
    
    # Handle case where classification might be a list
    if isinstance(classification, list):
        classification = classification[0] if classification else "personal"
    
    # LangChain's QdrantStore expects qdrant_client.http.models.Filter objects
    conditions = [
        FieldCondition(
            key="metadata.file_type",
            match=MatchValue(value=classification)
        )
    ]

    
    if week_start:
        if isinstance(week_start, list):
            # Filter for documents where week_start is any of the values in the list
            if week_start:  # Check if list is not empty
                conditions.append(
                    FieldCondition(
                        key="metadata.week_start",
                        match=MatchAny(any=week_start)
                    )
                )
        else:
            # Single week_start value
            conditions.append(
                FieldCondition(
                    key="metadata.week_start",
                    match=MatchValue(value=week_start)
                )
            )
    
    return Filter(must=conditions)