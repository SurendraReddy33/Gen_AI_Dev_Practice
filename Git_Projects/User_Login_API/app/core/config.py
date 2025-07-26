import secrets
 
# Generate a secure random secret key (once, then use it)
SECRET_KEY = secrets.token_hex(32)
 