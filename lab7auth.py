import bcrypt
import os

# Step 6: Define the User Data File
USER_DATA_FILE = "users.txt"

# Step 4: Implement Password Hashing
def hash_password(plain_text_password):
    # Encode the password to bytes (bcrypt requires byte strings)
    password_bytes = plain_text_password.encode('utf-8')
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Decode hash back to a string for storage
    return hashed.decode('utf-8')

# Step 5: Implement Password Verification
def verify_password(plain_text_password, hashed_password):
    # Encode both to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hash_bytes = hashed_password.encode('utf-8')
    # Compare using bcrypt
    return bcrypt.checkpw(password_bytes, hash_bytes)

# Step 8: Check if a username already exists
def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            stored_username, _ = line.strip().split(",", 1)
            if stored_username == username:
                return True
    return False

# Step 7: Register a new user
def register_user(username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    hashed = hash_password(password)
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed}\n")
    print(f"Success: User '{username}' registered successfully!")
    return True

# Step 9: Login function
def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False
    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            stored_username, stored_hash = line.strip().split(",", 1)
            if stored_username == username:
                if verify_password(password, stored_hash):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False
    print("Error: Username not found.")
    return False

# Step 10: Input validation
def validate_username(username):
    if not (3 <= len(username) <= 20):
        return False, "Username must be between 3 and 20 characters."
    if not username.isalnum():
        return False, "Username must contain only letters and numbers."
    return True, ""

def validate_password(password):
    if not (6 <= len(password) <= 50):
        return False, "Password must be between 6 and 50 characters."
    if not any(c.isupper() for c in password):
        return False, "Password must include at least one uppercase letter."
    if not any(c.islower() for c in password):
        return False, "Password must include at least one lowercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must include at least one number."
    return True, ""

# Step 11: Main menu interface
def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            register_user(username, password)

        elif choice == '2':
            # Login
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            login_user(username, password)
            input("\nPress Enter to return to main menu...")

        elif choice == '3':
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()

