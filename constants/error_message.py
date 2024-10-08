class ErrorMessage:
    REDIS_CONNECTION = "redis connection"
    REDIS_GET = "redis get data"
    REDIS_SET = "redis set data"
    MOCKSERVICE = "mock service does not respond"
    NOT_FOUND = "not found"
    EXTERNAL_SERVICE= "external service unavailable"
    PHONE_NUMBER_TAKEN = "this phone number is already registered with another account."
    BAD_CREDENTIALS = "credentials failed, incorrect username or password"
    INACTIVE_USER = "user is inactive"
    USER_NOT_FOUND = "user not found or inactive."
    REGISTRATION_FAILED = "something went wrong during user registration, please try again later."
    REQUEST_ERROR = "request error happened."
    REQUEST_TIMEOUT = "request timeout happened."
    CONNECTION_ERROR = "connection error happened."
    INVALID_CODE = "code is not valid or it's expired."
    INVALID_TOKEN = "token is invalid or expired."
    INVALID_TOKEN_FORMAT = "invalid authorization header format."
    INVALID_TOKEN_EXPIRED = "token has expired."
    MISSING_USER_PHONE_IN_HEADER = "missing user phone number in the request header."
    AUTHENTICATION_REQUIRED = "authentication required."
    INSUFFICIENT_PRIVILEGES = "insufficient privileges to perform this operation."


