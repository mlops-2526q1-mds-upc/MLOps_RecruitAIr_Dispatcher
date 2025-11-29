from . import extractor_worker

if __name__ == "__main__":
    import asyncio

    asyncio.run(extractor_worker())
