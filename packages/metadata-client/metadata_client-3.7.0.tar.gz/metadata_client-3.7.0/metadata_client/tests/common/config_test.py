"""Program Configuration variables"""

RESOURCE_NOT_FOUND = 'Resource not found!'

##########################################################################
#
# APPLICATION MODULES
#
##########################################################################
DATA_FILE = 'data_file'
DATA_GROUP = 'data_group'
DATA_GROUP_REPOSITORY = 'data_group_repository'
DATA_GROUP_TYPE = 'data_group_type'
DATA_TYPE = 'data_type'
EXPERIMENT = 'experiment'
EXPERIMENT_TYPE = 'experiment_type'
FACILITY = 'facility'
FILE_FORMAT = 'file_format'
INSTRUMENT = 'instrument'
INSTRUMENT_CYCLE = 'instrument_cycle'
INSTRUMENT_TYPE = 'instrument_type'
GROUP = 'group'
PARAMETER = 'parameter'
PARAMETER_TYPE = 'parameter_type'
PROPOSAL = 'proposal'
PROPOSALS_USER = 'proposals_user'
REPOSITORY = 'repository'
RUN = 'run'
RUN_DATA_GROUP = 'run_data_group'
SAMPLE = 'sample'
SAMPLE_TYPE = 'sample_type'
DARK_RUN = 'dark_run'

##########################################################################
#
# API PAGINATION
#
##########################################################################
DEF_PAGE = 1
DEF_PAGE_SIZE = 100

##########################################################################
#
# OAUTH2_XFEL_CLIENT (defaults)
#
##########################################################################
DEF_MAX_RETRIES = 3
DEF_TIMEOUT = 12
DEF_SSL_VERIFY = True

##########################################################################
#
# ACTIONS
#
##########################################################################
CREATE = 'CREATE'
DELETE = 'DELETE'
UPDATE = 'UPDATE'
GET = 'GET'

##########################################################################
#
# VARIABLES TYPES
#
##########################################################################
STRING = 'string'
NUMBER = 'number'
DOUBLE = 'double'
BOOLEAN = 'boolean'
DATETIME = 'datetime'

##########################################################################
#
# STATUS_CODE => https://docs.python.org/3/library/http.client.html
#
##########################################################################

# status codes informational
CONTINUE = 100
SWITCHING_PROTOCOLS = 101
PROCESSING = 102

# successful
OK = 200
CREATED = 201
ACCEPTED = 202
NON_AUTHORITATIVE_INFORMATION = 203
NO_CONTENT = 204
RESET_CONTENT = 205
PARTIAL_CONTENT = 206
MULTI_STATUS = 207
IM_USED = 226

# redirection
MULTIPLE_CHOICES = 300
MOVED_PERMANENTLY = 301
FOUND = 302
SEE_OTHER = 303
NOT_MODIFIED = 304
USE_PROXY = 305
TEMPORARY_REDIRECT = 307

# client error
BAD_REQUEST = 400
UNAUTHORIZED = 401
PAYMENT_REQUIRED = 402
FORBIDDEN = 403
NOT_FOUND = 404
METHOD_NOT_ALLOWED = 405
NOT_ACCEPTABLE = 406
PROXY_AUTHENTICATION_REQUIRED = 407
REQUEST_TIMEOUT = 408
CONFLICT = 409
GONE = 410
LENGTH_REQUIRED = 411
PRECONDITION_FAILED = 412
REQUEST_ENTITY_TOO_LARGE = 413
REQUEST_URI_TOO_LONG = 414
UNSUPPORTED_MEDIA_TYPE = 415
REQUESTED_RANGE_NOT_SATISFIABLE = 416
EXPECTATION_FAILED = 417
UNPROCESSABLE_ENTITY = 422
LOCKED = 423
FAILED_DEPENDENCY = 424
UPGRADE_REQUIRED = 426
PRECONDITION_REQUIRED = 428
TOO_MANY_REQUESTS = 429
REQUEST_HEADER_FIELDS_TOO_LARGE = 431

# server error
INTERNAL_SERVER_ERROR = 500
NOT_IMPLEMENTED = 501
BAD_GATEWAY = 502
SERVICE_UNAVAILABLE = 503
GATEWAY_TIMEOUT = 504
HTTP_VERSION_NOT_SUPPORTED = 505
INSUFFICIENT_STORAGE = 507
NOT_EXTENDED = 510
NETWORK_AUTHENTICATION_REQUIRED = 511
