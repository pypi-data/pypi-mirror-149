"""Test Configuration variables"""

# Note: URLs under https with a self-sign certificate
#       will only work if `ssl_verify == False`
# __APP_URL = 'https://127.0.0.1:8443/dev_metadata'

# Note: URLs under http
#       will only work if `OAUTHLIB_INSECURE_TRANSPORT=1`
# __APP_URL = 'http://127.0.0.1:3000/dev_metadata'

# Note: URLs under https with a valid certificate
#       issued by a certificate authority (CA)
#       will always work!!!
__APP_URL = 'https://in.xfel.eu/test_metadata'

###############################################################################
# Localhost setup:
#
# Listening on http://127.0.0.1:3000
# Listening on ssl://0.0.0.0:8443?cert=/Users/maial/development/gitlab/ITDM/metadata_catalog/config/certs/localhost.crt&key=/Users/maial/development/gitlab/ITDM/metadata_catalog/config/certs/localhost.key&verify_mode=none  # noqa
###############################################################################

# __USER_EMAIL = 'luis.maia@xfel.eu'
# __CLIENT_ID = '201ed15ff071a63e76cb0b91a1ab17b36d5f92d24b6df4497aa646e39c46a324'  # noqa
# __CLIENT_SECRET = 'a8ae80f5e96531f19bf2d2b6102f5a537196aca44a673ad36533310e07529757'  # noqa

###############################################################################
# Remote setup:
#
# Listening on https://in.xfel.eu/test_metadata
###############################################################################

__USER_EMAIL = 'luis.maia@xfel.eu'
__CLIENT_ID = '1cc9d1cd5e2752c26df9aa84d64927505ce43305ecc7c388d9b54e1f4deb3aab'  # noqa
__CLIENT_SECRET = '84b7295a40d8711b19eac7995a7d3e6b5c416a71dd11b9e033e46302aefe3925'  # noqa

###############################################################################

__OAUTH_TOKEN_URL = '{0}/oauth/token'.format(__APP_URL)
__OAUTH_AUTHORIZE_URL = '{0}/oauth/authorize'.format(__APP_URL)

###############################################################################
#
# Publicly available Variables (Test Purposes)
#
###############################################################################

# OAUTH2 client info used on Unitary tests
CLIENT_OAUTH2_INFO = {
    'EMAIL': __USER_EMAIL,
    'CLIENT_ID': __CLIENT_ID,
    'CLIENT_SECRET': __CLIENT_SECRET,
    #
    'AUTH_URL': __OAUTH_AUTHORIZE_URL,
    'TOKEN_URL': __OAUTH_TOKEN_URL,
    'REFRESH_URL': __OAUTH_TOKEN_URL,
    'SCOPE': '',
}

# User client info used on Unitary tests
USER_INFO = {
    'EMAIL': __USER_EMAIL,
    'FIRST_NAME': 'Luis',
    'LAST_NAME': 'Maia',
    'NAME': 'Luis Maia',
    'NICKNAME': 'maial',
    'PROVIDER': 'ldap',
    'UID': 'maial'
}

###############################################################################
#
# Publicly available Variables (Configuration Purposes)
#
###############################################################################

BASE_API_URL = '{0}/api/'.format(__APP_URL)
