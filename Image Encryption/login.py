import hashlib
import os

# Function to create a new user
def create_user():
    # Get username and password from user input
    username = input("Enter username: ")
    password = input("Enter password: ")

    if not username or not password:
        print("Username and password are required!")
        return

    # Hash username and password
    username_hash = hashlib.sha256(username.encode()).hexdigest()
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Create user folder if it doesn't exist
    user_folder = os.path.join('data/users', username_hash)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # Define the paths to save username and password hashes
    username_file = os.path.join(user_folder, 'username.txt')
    password_file = os.path.join(user_folder, 'password.txt')

    # Save the username and password hashes to the corresponding files
    with open(username_file, 'w') as f:
        f.write(username_hash)
    with open(password_file, 'w') as f:
        f.write(password_hash)

    print("User registered successfully!")

# Function to login an existing user
def login_user():
    # Get username and password from user input
    username = input("Enter username: ")
    password = input("Enter password: ")

    if not username or not password:
        print("Username and password are required!")
        return

    # Hash username and password
    username_hash = hashlib.sha256(username.encode()).hexdigest()
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Check if the user's folder exists
    user_folder = os.path.join('data/users', username_hash)
    if not os.path.exists(user_folder):
        print("Invalid username or password")
        return

    # Define the paths to read the stored username and password hashes
    username_file = os.path.join(user_folder, 'username.txt')
    password_file = os.path.join(user_folder, 'password.txt')

    # Read the stored username and password hashes
    with open(username_file, 'r') as f:
        stored_username_hash = f.read().strip()
    with open(password_file, 'r') as f:
        stored_password_hash = f.read().strip()

    # Compare the entered hashes with the stored hashes
    if stored_username_hash == username_hash and stored_password_hash == password_hash:
        print("Login successful!")
    else:
        print("Invalid username or password")

# Main function to choose between registering or logging in
def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter choice (1/2/3): ")

        if choice == '1':
            create_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    # Make sure the 'data/users' folder exists before using it
    if not os.path.exists('data/users'):
        os.makedirs('data/users')

    main()
