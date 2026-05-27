import os
import sys
import csv
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from platform_app.models import TeamProgress, BonusSubmission, PointAdjustment

def empty_database():
    TeamProgress.objects.all().delete()
    BonusSubmission.objects.all().delete()
    PointAdjustment.objects.all().delete()
    User.objects.exclude(username="aarush").delete()
    print("Database cleared (all users except aarush and all submissions removed).")

def add_superuser():
    username = input("Enter superuser username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    if User.objects.filter(username=username).exists():
        print("User already exists.")
        return
    email = input("Enter email (optional): ").strip()
    password = input("Enter password: ").strip()
    if not password:
        print("Password cannot be empty.")
        return
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully.")

def add_normal_user():
    username = input("Enter username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    if User.objects.filter(username=username).exists():
        print("User already exists.")
        return
    password = input("Enter password: ").strip()
    if not password:
        print("Password cannot be empty.")
        return
    User.objects.create_user(username=username, password=password)
    print(f"User '{username}' created successfully.")

def add_users_from_csv():
    path = input("Enter CSV file path: ").strip()
    if not os.path.exists(path):
        print("File does not exist.")
        return
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        if not rows:
            print("CSV file is empty.")
            return
        
        first_row = [col.lower().strip() for col in rows[0]]
        user_idx = 0
        pass_idx = 1
        
        has_header = False
        if any(h in first_row for h in ['user', 'username', 'login', 'name', 'password', 'pass']):
            has_header = True
            for idx, col in enumerate(first_row):
                if col in ['user', 'username', 'login', 'name']:
                    user_idx = idx
                elif col in ['password', 'pass']:
                    pass_idx = idx
        
        start_row = 1 if has_header else 0
        created_count = 0
        already_exists_count = 0
        
        for row in rows[start_row:]:
            if len(row) <= max(user_idx, pass_idx):
                continue
            username = row[user_idx].strip()
            password = row[pass_idx].strip()
            if not username or not password:
                continue
            if User.objects.filter(username=username).exists():
                already_exists_count += 1
                continue
            User.objects.create_user(username=username, password=password)
            created_count += 1
            
        print(f"Successfully added {created_count} users. ({already_exists_count} users already existed).")
    except Exception as e:
        print(f"Error reading CSV: {e}")

def main():
    while True:
        print("\nDIS Database Administrator Panel")
        print("1. Empty database (except aarush)")
        print("2. Add superuser")
        print("3. Add normal user")
        print("4. Add multiple users via csv")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()
        if choice == '1':
            empty_database()
        elif choice == '2':
            add_superuser()
        elif choice == '3':
            add_normal_user()
        elif choice == '4':
            add_users_from_csv()
        elif choice == '5':
            print("Exiting.")
            break
        else:
            print("Invalid selection. Please choose between 1 and 5.")

if __name__ == "__main__":
    main()
