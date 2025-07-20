from werkzeug.security import generate_password_hash

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python hash_password.py <password>")
        sys.exit(1)
    password = sys.argv[1]
    hashed = generate_password_hash(password)
    print(f"Hashed password: {hashed}") 