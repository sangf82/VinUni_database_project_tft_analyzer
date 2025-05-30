from werkzeug.security import generate_password_hash

def hash_password(password):
    """Generate a password hash from a plain text password"""
    return generate_password_hash(password)

# Example usage
password_to_hash = "123456"
hashed_result = hash_password(password_to_hash)
print(f"Password: {password_to_hash}")
print(f"Hash: {hashed_result}")
