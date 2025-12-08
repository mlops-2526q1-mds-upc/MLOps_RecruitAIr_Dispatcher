from prometheus_client import start_http_server

from . import evaluator_worker, settings

if __name__ == "__main__":
    import asyncio
    import logging

    logging.basicConfig(level=logging.INFO)

    if settings.expose_metrics:
        start_http_server(settings.metrics_server_port)
    asyncio.run(evaluator_worker())
