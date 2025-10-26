#!/usr/bin/env python3
"""
Seed script to create initial admin user
Run this once after setting up the database
"""

import sys
from utils.db import create_tables, add_user, generate_access_key

def seed_admin(email=None):
    # Create tables first
    create_tables()

    # Generate admin key
    admin_key = generate_access_key()

    # Add admin user
    if add_user(admin_key, role='admin', email=email):
        print("Admin user created successfully!")
        print(f"Admin Access Key: {admin_key}")
        if email:
            print(f"Associated Email: {email}")
        print("Keep this key safe - it's needed to access the admin panel.")
        return admin_key
    else:
        print("Failed to create admin user. Key might already exist.")
        return None

if __name__ == "__main__":
    email = sys.argv[1] if len(sys.argv) > 1 else None
    seed_admin(email)