from prometheus_client import Counter, Histogram

extractor_batch_size = Histogram(
    "extractor_batch_size",
    "Number of job offers analyzed in a single batch",
    buckets=(1, 5, 10, 20, 50, 100, 200, 500, 1000),
)

extractor_batch_dispatch_duration = Histogram(
    "extractor_batch_dispatch_duration_seconds",
    "Duration of extractor batch dispatch calls in seconds",
)

extractor_single_dispatch_duration = Histogram(
    "extractor_single_dispatch_duration_seconds",
    "Duration of a single extractor dispatch call in seconds",
)

extractor_total_dispatches = Counter(
    "extractor_total_dispatches",
    "Total number of extractor dispatch attempts",
)

extractor_failed_dispatches = Counter(
    "extractor_failed_dispatches_total",
    "Total number of failed extractor dispatch attempts",
)

extractor_timeouts = Counter(
    "extractor_timeouts_total",
    "Total number of extractor dispatch attempts that timed out",
)

extractor_time_since_schedule = Histogram(
    "extractor_time_since_schedule_seconds",
    "Time since job offer was scheduled for extraction in seconds",
    buckets=(1, 5, 10, 20, 50, 100, 200, 500, 1000),
)

extractor_criteria_computed = Counter(
    "extractor_criteria_computed_total",
    "Total number of criteria successfully computed by the extractor service",
)

extractor_criteria_importance_value = Histogram(
    "extractor_criteria_importance_value",
    "Distribution of job offer analysis criteria assigned by the extractor service",
    buckets=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
)

extractor_criteria_description_length = Histogram(
    "extractor_criteria_description_length",
    "Distribution of the length of criteria descriptions in the job offer analyses",
    buckets=(10, 50, 100, 200, 500, 1000, 2000, 5000),
)
