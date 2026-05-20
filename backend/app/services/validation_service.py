"""
RFID validation service – tag allocation, boundary check, scan comparison.
"""
import uuid
from datetime import datetime, timezone

from datetime import datetime, timezone
from bson import ObjectId
from app.extensions import get_db
from app.utils.constants import (
    TAG_STATUS_ACTIVE,
    SCAN_RESULT_MATCHED,
    SCAN_RESULT_UNMATCHED,
    SCAN_RESULT_SUSPICIOUS,
)


def generate_tag_ids(farmer_code: str, count: int) -> list:
    """Generate RFID tag IDs in format RFID-<FARMER_CODE>-<SEQ>.

    Args:
        farmer_code: Short code for the farmer (e.g. FARM001).
        count: Number of tags to generate.

    Returns:
        List of tag ID strings.
    """
    tags = []
    for i in range(1, count + 1):
        tag_id = f"RFID-{farmer_code}-{str(i).zfill(3)}"
        tags.append(tag_id)
    return tags


def allocate_tags(farmer_id: str, farmer_code: str, count: int) -> list:
    """Allocate RFID tags for a farmer and create boundary mapping.

    Returns:
        List of allocated tag documents.
    """
    db = get_db()
    tag_ids = generate_tag_ids(farmer_code, count)
    now = datetime.now(timezone.utc)
    tag_docs = []

    for tag_id in tag_ids:
        doc = {
            "tag_id": tag_id,
            "farmer_id": ObjectId(farmer_id) if isinstance(farmer_id, str) else farmer_id,
            "status": TAG_STATUS_ACTIVE,
            "allocated_at": now,
            "last_scanned": None,
        }
        # Upsert to avoid duplicates
        db.rfid_tags.update_one(
            {"tag_id": tag_id},
            {"$set": doc},
            upsert=True,
        )
        tag_docs.append(doc)

    # Create / update boundary mapping
    db.rfid_boundaries.update_one(
        {"farmer_id": ObjectId(farmer_id) if isinstance(farmer_id, str) else farmer_id},
        {
            "$set": {
                "farmer_id": ObjectId(farmer_id) if isinstance(farmer_id, str) else farmer_id,
                "tag_ids": tag_ids,
                "updated_at": now,
            }
        },
        upsert=True,
    )

    return tag_docs


def check_boundary(farmer_id: str, scanned_tag_id: str) -> str:
    """Check if a scanned tag belongs to the farmer's boundary.

    Returns:
        SCAN_RESULT_MATCHED  – tag belongs to this farmer
        SCAN_RESULT_UNMATCHED – tag doesn't belong to any farmer
        SCAN_RESULT_SUSPICIOUS – tag belongs to a DIFFERENT farmer
    """
    db = get_db()
    f_id = ObjectId(farmer_id) if isinstance(farmer_id, str) else farmer_id
    boundary = db.rfid_boundaries.find_one({"farmer_id": f_id})
    if not boundary:
        return SCAN_RESULT_UNMATCHED

    if scanned_tag_id in boundary.get("tag_ids", []):
        return SCAN_RESULT_MATCHED

    # Check if it belongs to someone else
    other = db.rfid_boundaries.find_one({
        "farmer_id": {"$ne": f_id},
        "tag_ids": scanned_tag_id,
    })
    if other:
        return SCAN_RESULT_SUSPICIOUS

    return SCAN_RESULT_UNMATCHED


def compare_scan_results(farmer_id: str, scanned_tags: list) -> dict:
    """Compare a list of scanned tags against the farmer's allocated boundary.

    Returns:
        {
            "matched": [...],
            "unmatched": [...],
            "suspicious": [...],
            "missing": [...],       # allocated but not scanned
            "total_allocated": int,
            "attendance_pct": float,
        }
    """
    db = get_db()
    f_id = ObjectId(farmer_id) if isinstance(farmer_id, str) else farmer_id
    boundary = db.rfid_boundaries.find_one({"farmer_id": f_id})
    allocated = set(boundary.get("tag_ids", [])) if boundary else set()

    matched = []
    unmatched = []
    suspicious = []

    for tag in scanned_tags:
        result = check_boundary(f_id, tag)
        if result == SCAN_RESULT_MATCHED:
            matched.append(tag)
        elif result == SCAN_RESULT_SUSPICIOUS:
            suspicious.append(tag)
        else:
            unmatched.append(tag)

    missing = list(allocated - set(matched))
    total = len(allocated) if allocated else 1
    attendance_pct = round((len(matched) / total) * 100, 2) if total else 0.0

    return {
        "matched": matched,
        "unmatched": unmatched,
        "suspicious": suspicious,
        "missing": missing,
        "total_allocated": len(allocated),
        "total_scanned": len(scanned_tags),
        "attendance_pct": attendance_pct,
    }


def validate_scan_session(session_id: str) -> dict:
    """Validate scan session and compute matched, unmatched, suspicious, and missing tags."""
    db = get_db()
    s_id = ObjectId(session_id) if isinstance(session_id, str) else session_id
    session = db.scan_sessions.find_one({"_id": s_id})
    if not session:
        raise ValueError("Scan session not found")

    scanned_tags = session.get("scanned_tags", [])
    farmer_id = session.get("farmer_id")

    res = compare_scan_results(farmer_id, scanned_tags)
    return {
        "matched": res["matched"],
        "unmatched": res["unmatched"],
        "suspicious": res["suspicious"],
        "missing": res["missing"],
        "summary": {
            "total_allocated": res["total_allocated"],
            "total_scanned": res["total_scanned"],
            "attendance_pct": res["attendance_pct"]
        }
    }

