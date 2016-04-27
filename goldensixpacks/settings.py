DEBUG = True
SECRET_KEY = 'this-june-will-be-too-hot'

# MongoDB Config
MONGODB_DB = 'goldensixpacks'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

# Flask-security Config
SECURITY_REGISTERABLE = False
SECURITY_CHANGEABLE = False
SECURITY_PASSWORD_HASH = "plaintext"  # "sha512_crypt"
SECURITY_PASSWORD_SALT = "MMMMM...SALTY"
