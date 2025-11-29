from . import evaluator_worker

if __name__ == "__main__":
    import asyncio
    import logging

    logging.basicConfig(level=logging.INFO)

    asyncio.run(evaluator_worker())
