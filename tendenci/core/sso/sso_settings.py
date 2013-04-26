from django.conf import settings

# Default user password for sso local users
try:
    SSO_DEFAULT_USER_PASSWORD = settings.SSO_DEFAULT_USER_PASSWORD
except:
    SSO_DEFAULT_USER_PASSWORD = settings.SECRET_KEY[::-1]


# If using relative paths, be careful!
try:
    SSO_CERTIFICATE_FILE = settings.SSO_CERTIFICATE_FILE
except:
    SSO_CERTIFICATE_FILE = 'keys/certificate.pem'


# If using relative paths, be careful!
try:
    SSO_PRIVATE_KEY_FILE = settings.SSO_PRIVATE_KEY_FILE
except:
    SSO_PRIVATE_KEY_FILE = 'keys/private-key.pem'
