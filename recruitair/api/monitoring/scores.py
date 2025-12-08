from prometheus_client import Counter, Histogram

SCORE_VALUES = Histogram(
    "applicant_score_values",
    "Values of applicant scores in API",
    buckets=(0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
)


GET_SCORES_REQUESTS = Counter("get_applicant_scores_requests_total", "Total number of get applicant scores requests")
GET_SCORES_REQUESTS_ERRORS = Counter(
    "get_applicant_scores_requests_errors_total",
    "Total number of get applicant scores requests that resulted in errors",
)
GET_SCORES_REQUESTS_TIME = Histogram(
    "get_applicant_scores_requests_time_seconds", "Time spent processing get applicant scores requests"
)
GET_SCORES_RETURNED_PER_REQUEST = Histogram(
    "get_applicant_scores_returned_per_request",
    "Number of scores returned per get applicant scores request",
    buckets=(1, 5, 10, 20, 50, 100, 200, 500, 1000),
)


GET_SCORE_REQUESTS = Counter("get_applicant_score_requests_total", "Total number of get applicant score requests")
GET_SCORE_REQUESTS_ERRORS = Counter(
    "get_applicant_score_requests_errors_total", "Total number of get applicant score requests that resulted in errors"
)
GET_SCORE_REQUESTS_TIME = Histogram(
    "get_applicant_score_requests_time_seconds", "Time spent processing get applicant score requests"
)


UPDATE_SCORE_REQUESTS = Counter(
    "update_applicant_score_requests_total", "Total number of update applicant score requests"
)
UPDATE_SCORE_REQUESTS_ERRORS = Counter(
    "update_applicant_score_requests_errors_total",
    "Total number of update applicant score requests that resulted in errors",
)
UPDATE_SCORE_REQUESTS_TIME = Histogram(
    "update_applicant_score_requests_time_seconds", "Time spent processing update applicant score requests"
)
UPDATE_SCORE_VALUE_DIFFERENCE = Histogram(
    "update_applicant_score_value_difference",
    "Difference in value when updating applicant scores",
    buckets=(
        -1,
        -0.9,
        -0.8,
        -0.7,
        -0.6,
        -0.5,
        -0.4,
        -0.3,
        -0.2,
        -0.1,
        0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1.0,
    ),
)
