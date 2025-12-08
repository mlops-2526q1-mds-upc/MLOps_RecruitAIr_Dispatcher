from prometheus_client import Counter, Histogram

CREATE_APPLICANTS_REQUESTS = Counter("create_applicants_requests_total", "Total number of create applicants requests")
CREATE_APPLICANTS_REQUESTS_ERRORS = Counter(
    "create_applicants_requests_errors_total", "Total number of create applicants requests that resulted in errors"
)
CREATE_APPLICANTS_REQUESTS_TIME = Histogram(
    "create_applicants_requests_time_seconds", "Time spent processing create applicants requests"
)
APPLICANTS_CREATED = Counter("applicants_created_total", "Total number of applicants created")
APPLICANTS_CREATED_PER_REQUEST = Histogram(
    "applicants_created_per_request", "Number of applicants created per create applicants request"
)
APPLICANT_CV_LENGTH = Histogram("applicant_cv_length", "Length of applicant CVs")


GET_APPLICANTS_REQUESTS = Counter("get_applicants_requests_total", "Total number of get applicants requests")
GET_APPLICANTS_REQUESTS_ERRORS = Counter(
    "get_applicants_requests_errors_total", "Total number of get applicants requests that resulted in errors"
)
GET_APPLICANTS_REQUESTS_TIME = Histogram(
    "get_applicants_requests_time_seconds", "Time spent processing get applicants requests"
)
APPLICANTS_RETURNED_PER_REQUEST = Histogram(
    "applicants_returned_per_request", "Number of applicants returned per get applicants request"
)
