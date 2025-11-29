from . import evaluator_worker

if __name__ == "__main__":
    import asyncio

    asyncio.run(evaluator_worker())
