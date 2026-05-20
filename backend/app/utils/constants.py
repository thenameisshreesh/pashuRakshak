"""
Status codes, roles, rejection reasons and other application-wide constants.
"""

# ─── User Roles ───────────────────────────────────────────────
ROLE_FARMER = "farmer"
ROLE_OFFICER = "officer"
ROLE_ADMIN = "admin"

ALL_ROLES = [ROLE_FARMER, ROLE_OFFICER, ROLE_ADMIN]
STAFF_ROLES = [ROLE_OFFICER, ROLE_ADMIN]

# ─── Application Status Flow ─────────────────────────────────
STATUS_PENDING = "pending"
STATUS_UNDER_REVIEW = "under_review"
STATUS_APPROVED = "approved"
STATUS_REJECTED = "rejected"
STATUS_RESUBMITTED = "resubmitted"

APPLICATION_STATUSES = [
    STATUS_PENDING,
    STATUS_UNDER_REVIEW,
    STATUS_APPROVED,
    STATUS_REJECTED,
    STATUS_RESUBMITTED,
]

# ─── Rejection Reasons (Dropdown) ────────────────────────────
REJECTION_REASONS = [
    "Insufficient cattle count",
    "Invalid or expired documents",
    "Land records mismatch",
    "Duplicate application detected",
    "Incomplete documentation",
    "Failed RFID validation",
    "Farmer not eligible for this scheme",
    "Suspicious cattle records",
    "Farm inspection failed",
    "Other (specify in notes)",
]

# ─── RFID / Scanning ─────────────────────────────────────────
TAG_STATUS_ACTIVE = "active"
TAG_STATUS_INACTIVE = "inactive"
TAG_STATUS_LOST = "lost"

SCAN_RESULT_MATCHED = "matched"
SCAN_RESULT_UNMATCHED = "unmatched"
SCAN_RESULT_SUSPICIOUS = "suspicious"

# ─── Raid Statuses ────────────────────────────────────────────
RAID_SCHEDULED = "scheduled"
RAID_IN_PROGRESS = "in_progress"
RAID_COMPLETED = "completed"
RAID_CANCELLED = "cancelled"

RAID_STATUSES = [RAID_SCHEDULED, RAID_IN_PROGRESS, RAID_COMPLETED, RAID_CANCELLED]

# ─── Notification Types ──────────────────────────────────────
NOTIF_APPLICATION_STATUS = "application_status"
NOTIF_RAID_SCHEDULED = "raid_scheduled"
NOTIF_VALIDATION_COMPLETE = "validation_complete"
NOTIF_GENERAL = "general"
NOTIF_TAG_ALLOCATED = "tag_allocated"

# ─── Audit Actions ───────────────────────────────────────────
AUDIT_LOGIN = "user_login"
AUDIT_REGISTER = "user_register"
AUDIT_APPLICATION_SUBMIT = "application_submit"
AUDIT_APPLICATION_UPDATE = "application_update"
AUDIT_APPLICATION_APPROVE = "application_approve"
AUDIT_APPLICATION_REJECT = "application_reject"
AUDIT_TAG_ALLOCATE = "tag_allocation"
AUDIT_RAID_SCHEDULE = "raid_schedule"
AUDIT_SCAN_START = "scan_session_start"
AUDIT_SCAN_END = "scan_session_end"

# ─── Allowed File Types ──────────────────────────────────────
ALLOWED_MIME_TYPES = [
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp",
    "video/mp4",
    "video/mpeg",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "audio/mpeg",
    "audio/wav",
    "audio/ogg",
]

# ─── Document Types ──────────────────────────────────────────
DOC_TYPE_AADHAAR = "aadhaar"
DOC_TYPE_PAN = "pan"
DOC_TYPE_LAND_RECORD = "land_record"
DOC_TYPE_CATTLE_PHOTO = "cattle_photo"
DOC_TYPE_CATTLE_VIDEO = "cattle_video"
DOC_TYPE_BANK_PASSBOOK = "bank_passbook"
DOC_TYPE_VACCINATION_CERT = "vaccination_certificate"
DOC_TYPE_OTHER = "other"

DOCUMENT_TYPES = [
    DOC_TYPE_AADHAAR,
    DOC_TYPE_PAN,
    DOC_TYPE_LAND_RECORD,
    DOC_TYPE_CATTLE_PHOTO,
    DOC_TYPE_CATTLE_VIDEO,
    DOC_TYPE_BANK_PASSBOOK,
    DOC_TYPE_VACCINATION_CERT,
    DOC_TYPE_OTHER,
]

# ─── Scheme Application Steps ────────────────────────────────
STEP_BASIC_DETAILS = 1
STEP_DOCUMENTS = 2
STEP_CATTLE_PROOF = 3
TOTAL_STEPS = 3
