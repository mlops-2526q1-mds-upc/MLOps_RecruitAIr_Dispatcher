from prometheus_client import Counter, Histogram

CREATE_CRITERIA_REQUESTS = Counter("create_criteria_requests_total", "Total number of create criteria requests")
CREATE_CRITERIA_REQUESTS_ERRORS = Counter(
    "create_criteria_requests_errors_total", "Total number of create criteria requests that resulted in errors"
)
CREATE_CRITERIA_REQUESTS_TIME = Histogram(
    "create_criteria_requests_time_seconds", "Time spent processing create criteria requests"
)
CREATE_CRITERIA_DESCRIPTION_LENGTH = Histogram(
    "create_criteria_description_length", "Length of created criteria descriptions in API"
)
CREATE_CRITERIA_IMPORTANCE = Histogram("create_criteria_importance", "Importance of created criteria in API")
CRITERIA_CREATED = Counter("criteria_created_total", "Total number of criteria created")
CRITERIA_CREATED_PER_REQUEST = Histogram(
    "criteria_created_per_request", "Number of criteria created per create criteria request"
)


GET_CRITERIA_REQUESTS = Counter("get_criteria_requests_total", "Total number of get criteria requests")
GET_CRITERIA_REQUESTS_ERRORS = Counter(
    "get_criteria_requests_errors_total", "Total number of get criteria requests that resulted in errors"
)
GET_CRITERIA_REQUESTS_TIME = Histogram(
    "get_criteria_requests_time_seconds", "Time spent processing get criteria requests"
)
GET_CRITERIA_RETURNED_PER_REQUEST = Histogram(
    "get_criteria_returned_per_request", "Number of criteria returned per get criteria request"
)


UPDATE_CRITERION_REQUESTS = Counter("update_criterion_requests_total", "Total number of update criterion requests")
UPDATE_CRITERION_REQUESTS_ERRORS = Counter(
    "update_criterion_requests_errors_total", "Total number of update criterion requests that resulted in errors"
)
UPDATE_CRITERION_REQUESTS_TIME = Histogram(
    "update_criterion_requests_time_seconds", "Time spent processing update criterion requests"
)
UPDATE_CRITERION_DESCRIPTION_LENGTH = Histogram(
    "update_criterion_description_length", "Length of updated criterion descriptions in API"
)
UPDATE_CRITERION_IMPORTANCE = Histogram("update_criterion_importance", "Importance of updated criteria in API")
