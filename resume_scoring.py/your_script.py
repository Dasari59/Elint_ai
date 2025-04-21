import os

# Retrieve the credentials securely
sender_email = os.getenv("EMAIL_USER")  # Get email stored in environment variables
sender_password = os.getenv("EMAIL_PASS")  # Get password stored in environment variables

# Print values (Avoid printing passwords in production!)
print(f"Sender Email: {sender_email}")
print(f"Sender Password: {sender_password}")  # Remove this in production for security