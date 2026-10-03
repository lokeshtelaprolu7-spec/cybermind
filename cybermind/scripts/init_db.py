#!/usr/bin/env python3
"""
CyberMIND Database Initialization & Migration Utility
Connects to DATABASE_URL, initializes all relational tables, and loads
authoritative knowledge base (and demo data if DEMO_MODE=true).
"""

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.core.config import settings
from app.database.session import Base, engine, SessionLocal
import app.models  # Register all models with Base
from app.services.seed import seed_demo_organization, seed_knowledge_base
from sqlalchemy import text, inspect

def initialize_database():
    print("=" * 60)
    print(" [CYBERMIND] Database Initializer")
    print("=" * 60)
    print(f"[*] Target Database Dialect: {engine.url.drivername}")
    print(f"[*] Environment: {settings.ENVIRONMENT}")
    print(f"[*] DEMO_MODE: {settings.DEMO_MODE}")

    # For PostgreSQL, check/enable extensions if possible
    if "postgres" in engine.url.drivername:
        print("[*] Checking PostgreSQL extensions...")
        try:
            with engine.connect() as conn:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))
                conn.commit()
                print("[+] Extension 'uuid-ossp' ensured.")
        except Exception as e:
            print(f"[!] Note on extensions: {e}")

    # Create all tables
    print("[*] Creating all schema tables...")
    Base.metadata.create_all(bind=engine)
    
    # Inspect tables created
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"[+] Total tables registered: {len(tables)}")
    for t in sorted(tables):
        print(f"    - {t}")

    # Seed data
    with SessionLocal() as db:
        if settings.DEMO_MODE:
            print("[*] DEMO_MODE is True: Seeding demo organization & synthetic assets...")
            seed_demo_organization(db)
            print("[+] Demo data seeded successfully.")
        else:
            print("[*] DEMO_MODE is False (Production): Seeding authoritative knowledge base only...")
            seed_knowledge_base(db)
            print("[+] Authoritative security knowledge base seeded successfully.")

    print("\n[SUCCESS] CyberMIND Database initialization complete and verified.")

if __name__ == "__main__":
    initialize_database()
