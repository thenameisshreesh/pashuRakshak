"""
Utility helpers for JSON serialization, datetime formatting, pagination, etc.
"""
from datetime import datetime, timezone
from bson import ObjectId


def now_utc() -> datetime:
    """Return timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


def serialize_doc(doc: dict) -> dict:
    """Convert a MongoDB document to a JSON-serializable dict.
    
    - Converts ObjectId fields to strings.
    - Converts datetime fields to ISO-format strings.
    """
    if doc is None:
        return {}
    result = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            result[key] = str(value)
        elif isinstance(value, datetime):
            result[key] = value.isoformat()
        elif isinstance(value, list):
            result[key] = [serialize_doc(v) if isinstance(v, dict) else (str(v) if isinstance(v, ObjectId) else v) for v in value]
        elif isinstance(value, dict):
            result[key] = serialize_doc(value)
        else:
            result[key] = value
    return result


def serialize_docs(docs) -> list:
    """Serialize a list/cursor of MongoDB documents."""
    return [serialize_doc(doc) for doc in docs]


def paginate_query(collection, query: dict, page: int = 1, per_page: int = 20, sort_field: str = "_id", sort_order: int = -1):
    """Paginate a MongoDB query and return results + metadata."""
    page = max(1, page)
    per_page = min(max(1, per_page), 100)
    skip = (page - 1) * per_page
    total = collection.count_documents(query)
    cursor = collection.find(query).sort(sort_field, sort_order).skip(skip).limit(per_page)
    items = serialize_docs(cursor)
    return {
        "items": items,
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total + per_page - 1) // per_page if per_page else 1,
    }


def to_object_id(id_str: str):
    """Safely convert a string to ObjectId, return None on failure."""
    try:
        return ObjectId(id_str)
    except Exception:
        return None


def make_response_body(success: bool, message: str = "", data=None, status_code: int = 200):
    """Build a standardised JSON response dict."""
    body = {"success": success, "message": message}
    if data is not None:
        body["data"] = data
    return body, status_code


def get_client_ip(request):
    """Extract client IP from request (handles proxies)."""
    if request.headers.get("X-Forwarded-For"):
        return request.headers["X-Forwarded-For"].split(",")[0].strip()
    return request.remote_addr or "unknown"


def paginate(cursor, request):
    """Paginate a PyMongo cursor based on request query parameters.
    
    Returns:
        list: The serialized items for the current page.
        dict: The pagination metadata.
    """
    try:
        page = int(request.args.get('page', 1))
    except (ValueError, TypeError):
        page = 1
    try:
        per_page = int(request.args.get('per_page', 20))
    except (ValueError, TypeError):
        per_page = 20
        
    page = max(1, page)
    per_page = min(max(1, per_page), 100)
    
    # In PyMongo 4, cursor.count() is removed. We fetch all items to get length and slice.
    # For this scale of project, this is simple and robust.
    all_items = list(cursor)
    total = len(all_items)
    items = all_items[(page - 1) * per_page : page * per_page]
    
    serialized_items = serialize_docs(items)
    pages = (total + per_page - 1) // per_page if per_page else 1
    
    return serialized_items, {
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": pages
    }

