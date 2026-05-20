"""
Seed data for PashuRakshak - 3 schemes, 3 farmers, 3 officers.
Auto-creates collections and inserts data on first run.
"""
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from .extensions import get_db


def init_seed_data():
    """Initialize database with seed data if collections are empty."""
    db = get_db()

    existing_collections = db.list_collection_names()

    # Seed officers/admin users
    if 'users' not in existing_collections or db.users.count_documents({"role": {"$in": ["admin", "officer"]}}) == 0:
        _seed_officers(db)

    # Seed farmer users
    if 'users' not in existing_collections or db.users.count_documents({"role": "farmer"}) == 0:
        _seed_farmers(db)

    # Seed schemes
    if 'schemes' not in existing_collections or db.schemes.count_documents({}) == 0:
        _seed_schemes(db)

    # Create indexes
    _create_indexes(db)

    print("[SEED] Database initialization complete.")


def _seed_officers(db):
    """Seed 3 government officers."""
    password_hash = generate_password_hash("pashurakshak123")

    officers = [
        {
            "name": "Amit Verma",
            "username": "admin",
            "mobile": "9000000001",
            "password_hash": password_hash,
            "role": "admin",
            "department": "Ministry of Animal Husbandry",
            "designation": "District Animal Husbandry Officer",
            "state": "Maharashtra",
            "district": "Mumbai",
            "created_at": datetime.utcnow(),
            "status": "active"
        },
        {
            "name": "Priya Singh",
            "username": "officer1",
            "mobile": "9000000002",
            "password_hash": password_hash,
            "role": "officer",
            "department": "State Animal Welfare Board",
            "designation": "Field Inspection Officer",
            "state": "Rajasthan",
            "district": "Jaipur",
            "created_at": datetime.utcnow(),
            "status": "active"
        },
        {
            "name": "Rahul Deshmukh",
            "username": "officer2",
            "mobile": "9000000003",
            "password_hash": password_hash,
            "role": "officer",
            "department": "NDDB Regional Office",
            "designation": "Livestock Verification Officer",
            "state": "Madhya Pradesh",
            "district": "Indore",
            "created_at": datetime.utcnow(),
            "status": "active"
        }
    ]

    result = db.users.insert_many(officers)
    print(f"[SEED] Inserted {len(result.inserted_ids)} officers.")


def _seed_farmers(db):
    """Seed 3 farmer profiles."""
    password_hash = generate_password_hash("pashurakshak123")

    farmers_users = [
        {
            "name": "Ramesh Patil",
            "mobile": "9876543210",
            "password_hash": password_hash,
            "role": "farmer",
            "language": "mr",
            "created_at": datetime.utcnow(),
            "status": "active"
        },
        {
            "name": "Suresh Kumar",
            "mobile": "9876543211",
            "password_hash": password_hash,
            "role": "farmer",
            "language": "hi",
            "created_at": datetime.utcnow(),
            "status": "active"
        },
        {
            "name": "Ganesh Sharma",
            "mobile": "9876543212",
            "password_hash": password_hash,
            "role": "farmer",
            "language": "en",
            "created_at": datetime.utcnow(),
            "status": "active"
        }
    ]

    user_results = db.users.insert_many(farmers_users)
    user_ids = user_results.inserted_ids

    # Create extended farmer profiles
    farmer_profiles = [
        {
            "user_id": user_ids[0],
            "name": "Ramesh Patil",
            "dob": datetime(1975, 3, 15),
            "age": 51,
            "mobile": "9876543210",
            "state": "Maharashtra",
            "district": "Pune",
            "acres": 15,
            "cattle_count": 75,
            "farmer_proof_file_id": None,
            "status": "verified",
            "created_at": datetime.utcnow()
        },
        {
            "user_id": user_ids[1],
            "name": "Suresh Kumar",
            "dob": datetime(1980, 7, 22),
            "age": 46,
            "mobile": "9876543211",
            "state": "Rajasthan",
            "district": "Jaipur",
            "acres": 25,
            "cattle_count": 120,
            "farmer_proof_file_id": None,
            "status": "verified",
            "created_at": datetime.utcnow()
        },
        {
            "user_id": user_ids[2],
            "name": "Ganesh Sharma",
            "dob": datetime(1968, 11, 5),
            "age": 57,
            "mobile": "9876543212",
            "state": "Madhya Pradesh",
            "district": "Indore",
            "acres": 50,
            "cattle_count": 250,
            "farmer_proof_file_id": None,
            "status": "verified",
            "created_at": datetime.utcnow()
        }
    ]

    result = db.farmers.insert_many(farmer_profiles)
    print(f"[SEED] Inserted {len(result.inserted_ids)} farmer profiles.")


def _seed_schemes(db):
    """Seed 3 government cattle schemes."""
    schemes = [
        {
            "name": "Rashtriya Gokul Mission",
            "motive": "Conservation and development of indigenous bovine breeds to enhance milk productivity and make dairying more remunerative to the rural farmer.",
            "eligibility": "Registered gaushalas and dairy farmers with minimum 50 indigenous breed cattle. Must have valid land documents and Aadhaar verification.",
            "sponsor": "Ministry of Animal Husbandry, Dairying & Fisheries, Government of India",
            "benefits": "Financial assistance up to ₹5,00,000 for breed improvement, fodder development, and veterinary care. Subsidized AI services and cattle insurance.",
            "description": "The Rashtriya Gokul Mission focuses on the development and conservation of indigenous bovine breeds. It aims to enhance productivity through breed improvement using scientific techniques. The mission supports establishing Gokul Grams as integrated cattle development centers.",
            "images": [],
            "required_validations": 3,
            "required_cattle_count": 50,
            "duration_days": 365,
            "start_date": datetime.utcnow(),
            "end_date": datetime.utcnow() + timedelta(days=365),
            "status": "active",
            "created_at": datetime.utcnow(),
            "created_by": "admin"
        },
        {
            "name": "National Dairy Plan Phase-II",
            "motive": "Increase productivity of milch animals and provide rural milk producers with greater access to the organized milk processing sector.",
            "eligibility": "Progressive dairy farmers and cooperatives with minimum 100 milch animals. Must demonstrate established milk collection infrastructure.",
            "sponsor": "National Dairy Development Board (NDDB)",
            "benefits": "Grant of ₹10,00,000 for ration balancing, AI services, milk testing equipment, and bulk milk coolers. Training and capacity building support.",
            "description": "National Dairy Plan Phase-II builds upon the success of NDP-I. It covers 18 major milk-producing states. The plan aims to strengthen milk procurement at the village level, improve quality of milk and milk products, and support producer institutions.",
            "images": [],
            "required_validations": 5,
            "required_cattle_count": 100,
            "duration_days": 730,
            "start_date": datetime.utcnow(),
            "end_date": datetime.utcnow() + timedelta(days=730),
            "status": "active",
            "created_at": datetime.utcnow(),
            "created_by": "admin"
        },
        {
            "name": "Gaushala Development Grant",
            "motive": "Support gaushalas in providing proper shelter, nutrition, and healthcare to rescued and abandoned cattle across the country.",
            "eligibility": "Registered gaushalas with minimum 200 cattle under care. Must have proper land registration, infrastructure, and veterinary staff.",
            "sponsor": "State Animal Welfare Board",
            "benefits": "Annual grant of ₹15,00,000 for infrastructure development, fodder procurement, veterinary services, and staff salaries. Additional emergency medical fund.",
            "description": "The Gaushala Development Grant scheme provides financial assistance to registered gaushalas for the welfare and maintenance of cattle. The scheme covers construction of sheds, purchase of fodder, veterinary care, and staff training. Gaushalas must maintain detailed records of all cattle.",
            "images": [],
            "required_validations": 4,
            "required_cattle_count": 200,
            "duration_days": 365,
            "start_date": datetime.utcnow(),
            "end_date": datetime.utcnow() + timedelta(days=365),
            "status": "active",
            "created_at": datetime.utcnow(),
            "created_by": "admin"
        }
    ]

    result = db.schemes.insert_many(schemes)
    print(f"[SEED] Inserted {len(result.inserted_ids)} schemes.")


def _create_indexes(db):
    """Create database indexes for performance."""
    # Users indexes
    db.users.create_index("mobile", unique=True, sparse=True)
    db.users.create_index("username", unique=True, sparse=True)
    db.users.create_index("role")

    # Farmers indexes
    db.farmers.create_index("user_id", unique=True)
    db.farmers.create_index("mobile", unique=True)
    db.farmers.create_index("state")
    db.farmers.create_index("district")

    # Schemes indexes
    db.schemes.create_index("status")
    db.schemes.create_index("created_at")

    # Applications indexes
    db.applications.create_index("farmer_id")
    db.applications.create_index("scheme_id")
    db.applications.create_index("status")
    db.applications.create_index([("farmer_id", 1), ("scheme_id", 1)])

    # RFID allocations indexes
    db.rfid_allocations.create_index("farmer_id")
    db.rfid_allocations.create_index("tag_ids")
    db.rfid_allocations.create_index([("farmer_id", 1), ("scheme_id", 1)])

    # Raids indexes
    db.raids.create_index("farmer_id")
    db.raids.create_index("officer_id")
    db.raids.create_index("status")
    db.raids.create_index("date")

    # Scan sessions indexes
    db.scan_sessions.create_index("raid_id")
    db.scan_sessions.create_index("status")

    # Scan logs indexes
    db.scan_logs.create_index("session_id")
    db.scan_logs.create_index("tag_id")

    # Notifications indexes
    db.notifications.create_index("user_id")
    db.notifications.create_index([("user_id", 1), ("read", 1)])
    db.notifications.create_index("created_at")

    # Audit logs indexes
    db.audit_logs.create_index("user_id")
    db.audit_logs.create_index("action")
    db.audit_logs.create_index("timestamp")

    print("[SEED] Database indexes created.")
