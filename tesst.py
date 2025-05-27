from werkzeug.security import generate_password_hash, check_password_hash

def set_password(self, password):
    """Hash and set the user's password"""
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    """Check if the provided password matches the stored hash"""
    return check_password_hash(self.password_hash, password)

# To find the origin of your hashed string, you'll need to try different passwords
hashed_password = "scrypt:32768:8:1$VxnWIz5zSryq0dCz$c98c017002df606736dd7b2c5f0e9c786a77bb7fa2221e0003203b3e155528b2d407978e9617d068f89e4cdde3f6dd39ea6123584273babbb94276b258a64eb2"

# Example usage to test passwords
def find_password_origin(hash_string, potential_passwords):
    """Test a list of potential passwords against the hash"""
    for password in potential_passwords:
        if check_password_hash(hash_string, password):
            return password
    return None

# Test common passwords
common_passwords = ["password", "123456", "admin", "test", "user", "player 3"]
original_password = find_password_origin(hashed_password, common_passwords)
print(f"Original password: {original_password}")