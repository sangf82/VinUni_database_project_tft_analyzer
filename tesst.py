from werkzeug.security import generate_password_hash, check_password_hash

def set_password(password):
    """Hash and set the user's password"""
    return generate_password_hash(password)

def check_password(password_hash, password):
    """Check if the provided password matches the stored hash"""
    return check_password_hash(password_hash, password)

# Example: Convert string to hash
password_to_hash = "123456"
hashed_password = set_password(password_to_hash)
print(f"Original password: {password_to_hash}")
print(f"Hashed password: {hashed_password}")

# Verify the password
is_correct = check_password(hashed_password, "player 3")
print(f"Password verification: {is_correct}")

# Your existing hash for testing
existing_hash = "scrypt:32768:8:1$VxnWIz5zSryq0dCz$c98c017002df606736dd7b2c5f0e9c786a77bb7fa2221e0003203b3e155528b2d407978e9617d068f89e4cdde3f6dd39ea6123584273babbb94276b258a64eb2"

# Function to find password origin
def find_password_origin(hash_string, potential_passwords):
    """Test a list of potential passwords against the hash"""
    for password in potential_passwords:
        if check_password_hash(hash_string, password):
            return password
    return None

# Test common passwords against existing hash
common_passwords = ["password", "123456", "admin", "test", "user", "player 3"]
original_password = find_password_origin(existing_hash, common_passwords)
print(f"Original password for existing hash: {original_password}")