from qdrant_client.http.models import Filter, FieldCondition, MatchValue, MatchAny

def create_search_filter(classification, week_start=None):
    # Normalize classification to list
    if not classification:
        classification = ["personal"]
    elif isinstance(classification, str):
        classification = [classification] if classification.strip() else ["personal"]
    elif isinstance(classification, list) and not classification:
        classification = ["personal"]
    
    # Clean up classification list
    classification = [cat.strip() for cat in classification if cat and cat.strip()]
    if not classification:
        classification = ["personal"]
    
    conditions = []
    
    # Handling multiple classifications with OR logic
    if len(classification) == 1:
        # Single classification
        conditions.append(
            FieldCondition(
                key="metadata.file_type",
                match=MatchValue(value=classification[0])
            )
        )
    else:
        # Multiple classifications - MatchAny for OR logic
        conditions.append(
            FieldCondition(
                key="metadata.file_type",
                match=MatchAny(any=classification)
            )
        )

    # Handle week_start filter
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
    
    filter = Filter(must=conditions)
    return filter