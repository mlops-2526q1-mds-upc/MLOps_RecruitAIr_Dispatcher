from prometheus_client import Counter, Histogram

evaluator_batch_obtaining_duration = Histogram(
    "evaluator_batch_obtaining_duration_seconds",
    "Duration of evaluator batch obtaining calls in seconds",
)

evaluator_batch_size = Histogram(
    "evaluator_batch_size",
    "Number of applicants evaluated in a single batch",
    buckets=(1, 5, 10, 20, 50, 100, 200, 500, 1000),
)

evaluator_batch_dispatch_duration = Histogram(
    "evaluator_batch_dispatch_duration_seconds",
    "Duration of evaluator batch dispatch calls in seconds",
)

evaluator_single_dispatch_duration = Histogram(
    "evaluator_single_dispatch_duration_seconds",
    "Duration of a single evaluator dispatch call in seconds",
)

evaluator_total_dispatches = Counter(
    "evaluator_total_dispatches",
    "Total number of evaluator dispatch attempts",
)

evaluator_failed_dispatches = Counter(
    "evaluator_failed_dispatches_total",
    "Total number of failed evaluator dispatch attempts",
)

evaluator_timeouts = Counter(
    "evaluator_timeouts_total",
    "Total number of evaluator dispatch attempts that timed out",
)

evaluator_time_since_schedule = Histogram(
    "evaluator_time_since_schedule_seconds",
    "Time since applicant or criteria was scheduled for evaluation in seconds",
    buckets=(1, 5, 10, 20, 50, 100, 200, 500, 1000),
)

evaluator_scores_computed = Counter(
    "evaluator_scores_computed_total",
    "Total number of applicant scores successfully computed by the evaluator service",
)

evaluator_score_value = Histogram(
    "evaluator_score_value",
    "Distribution of applicant scores assigned by the evaluator service",
    buckets=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
)
