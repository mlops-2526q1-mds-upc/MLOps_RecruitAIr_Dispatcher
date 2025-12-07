from prometheus_client import Counter, Summary

CREATE_OFFER_REQUESTS = Counter("create_job_offer_requests_total", "Total number of create job offer requests")
CREATE_OFFER_REQUESTS_ERRORS = Counter(
    "create_job_offer_requests_errors_total", "Total number of create job offer request errors"
)
CREATE_OFFER_REQUESTS_TIME = Summary(
    "create_job_offer_requests_time_seconds", "Time spent processing create job offer requests"
)
CREATED_OFFERS = Counter("job_offers_created_total", "Total number of job offers created")
CREATE_OFFER_TEXT_LENGTH = Summary("create_job_offer_text_length", "Length of created job offer texts")


LIST_OFFERS_REQUESTS = Counter("list_job_offers_requests_total", "Total number of list job offers requests")
LIST_OFFERS_REQUESTS_ERRORS = Counter(
    "list_job_offers_requests_errors_total", "Total number of list job offers request errors"
)
LIST_OFFERS_REQUESTS_TIME = Summary(
    "list_job_offers_requests_time_seconds", "Time spent processing list job offers requests"
)
LIST_OFFERS_RETURNED_PER_REQUEST = Summary(
    "list_job_offers_returned_per_request", "Number of job offers returned per list job offers request"
)

GET_OFFER_REQUESTS = Counter("get_job_offer_requests_total", "Total number of get job offer requests")
GET_OFFER_REQUESTS_ERRORS = Counter(
    "get_job_offer_requests_errors_total", "Total number of get job offer request errors"
)
GET_OFFER_REQUESTS_TIME = Summary("get_job_offer_requests_time_seconds", "Time spent processing get job offer requests")
