#!/usr/bin/env python3
"""
CyberMIND Production Admin Provisioning Script
Usage:
    python scripts/create_admin.py --email admin@example.com --password StrongPassword123! --full-name "SecOps Admin"
Or run interactively:
    python scripts/create_admin.py
"""

import sys
import os
import argparse
import getpass

# Add backend directory to sys.path so app imports work
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.database.session import SessionLocal, Base, engine
from app.models.entities import User, Organization
from app.core.security import get_password_hash

def provision_admin(email: str, password: str, full_name: str, org_name: str, role: str = "admin"):
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        # 1. Ensure target Organization exists
        org = db.query(Organization).filter(Organization.name == org_name).first()
        if not org:
            org = Organization(
                name=org_name,
                domain=org_name.lower().replace(" ", "") + ".internal",
                description="Primary Production Security Operations Organization"
            )
            db.add(org)
            db.commit()
            db.refresh(org)
            print(f"[+] Created Organization: '{org.name}' (ID: {org.id})")
        else:
            print(f"[*] Found existing Organization: '{org.name}' (ID: {org.id})")

        # 2. Check if user already exists
        existing_user = db.query(User).filter(User.email == email.lower()).first()
        if existing_user:
            print(f"[*] User '{email}' already exists. Updating credentials and elevating to '{role}'...")
            existing_user.hashed_password = get_password_hash(password)
            existing_user.full_name = full_name
            existing_user.role = role
            existing_user.organization_id = org.id
            existing_user.is_active = True
            db.commit()
            print(f"[SUCCESS] Successfully updated user '{email}' as '{role}'.")
            return

        # 3. Create new admin user
        hashed_pw = get_password_hash(password)
        new_admin = User(
            email=email.lower().strip(),
            hashed_password=hashed_pw,
            full_name=full_name,
            role=role,
            organization_id=org.id,
            is_active=True
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        print(f"[SUCCESS] Successfully created administrator user '{new_admin.email}' with role '{new_admin.role}'.")

def main():
    parser = argparse.ArgumentParser(description="Create or update CyberMIND Administrator")
    parser.add_argument("--email", help="Administrator email address")
    parser.add_argument("--password", help="Administrator password (prompted if omitted)")
    parser.add_argument("--full-name", default="CyberMIND Administrator", help="Full name of administrator")
    parser.add_argument("--org-name", default="CyberMIND Enterprise", help="Organization name")
    parser.add_argument("--role", default="admin", help="User role (admin, analyst, auditor)")
    
    args = parser.parse_args()

    email = args.email
    if not email:
        email = input("Enter admin email: ").strip()

    if not email or "@" not in email:
        print("[!] Error: A valid email address is required.", file=sys.stderr)
        sys.exit(1)

    password = args.password
    if not password:
        password = getpass.getpass("Enter admin password: ")
        confirm_password = getpass.getpass("Confirm admin password: ")
        if password != confirm_password:
            print("[!] Error: Passwords do not match.", file=sys.stderr)
            sys.exit(1)

    if len(password) < 8:
        print("[!] Error: Password must be at least 8 characters long.", file=sys.stderr)
        sys.exit(1)

    provision_admin(
        email=email,
        password=password,
        full_name=args.full_name,
        org_name=args.org_name,
        role=args.role
    )

if __name__ == "__main__":
    main()
