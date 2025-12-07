from prometheus_client import Counter, Summary

SCORE_VALUES = Summary("applicant_score_values", "Values of applicant scores in API")


GET_SCORES_REQUESTS = Counter("get_applicant_scores_requests_total", "Total number of get applicant scores requests")
GET_SCORES_REQUESTS_ERRORS = Counter(
    "get_applicant_scores_requests_errors_total",
    "Total number of get applicant scores requests that resulted in errors",
)
GET_SCORES_REQUESTS_TIME = Summary(
    "get_applicant_scores_requests_time_seconds", "Time spent processing get applicant scores requests"
)
GET_SCORES_RETURNED_PER_REQUEST = Summary(
    "get_applicant_scores_returned_per_request", "Number of scores returned per get applicant scores request"
)


GET_SCORE_REQUESTS = Counter("get_applicant_score_requests_total", "Total number of get applicant score requests")
GET_SCORE_REQUESTS_ERRORS = Counter(
    "get_applicant_score_requests_errors_total", "Total number of get applicant score requests that resulted in errors"
)
GET_SCORE_REQUESTS_TIME = Summary(
    "get_applicant_score_requests_time_seconds", "Time spent processing get applicant score requests"
)


UPDATE_SCORE_REQUESTS = Counter(
    "update_applicant_score_requests_total", "Total number of update applicant score requests"
)
UPDATE_SCORE_REQUESTS_ERRORS = Counter(
    "update_applicant_score_requests_errors_total",
    "Total number of update applicant score requests that resulted in errors",
)
UPDATE_SCORE_REQUESTS_TIME = Summary(
    "update_applicant_score_requests_time_seconds", "Time spent processing update applicant score requests"
)
UPDATE_SCORE_VALUE_DIFFERENCE = Summary(
    "update_applicant_score_value_difference", "Difference in value when updating applicant scores"
)
