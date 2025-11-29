import asyncio
import logging
import traceback
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .extractor_settings import ExtractorWorkerSettings

logger = logging.getLogger(__name__)
settings = ExtractorWorkerSettings()

from ...database import get_async_session
from ...database.models import JobOffer, JobOfferStatus
from .criteria_extraction import extract_criteria


async def get_batch(session: AsyncSession, batch_size: int) -> Sequence[JobOffer]:
    query = (
        select(JobOffer)
        .where(JobOffer.status == JobOfferStatus.PENDING)
        .order_by(JobOffer.created_at)
        .limit(batch_size)
        .with_for_update(skip_locked=True)
    )
    result = await session.execute(query)
    return result.scalars().all()


async def handle_job_offer(job_offer: JobOffer, session: AsyncSession):
    try:
        await extract_criteria(job_offer, session)
    except Exception as e:
        logger.error(f"Error processing job offer id {job_offer.id}: {e}")
        logger.error("Stack trace:")
        for line in traceback.format_exception(type(e), e, e.__traceback__):
            logger.error(line)


async def extractor_worker():
    logger.info(
        f"Starting Extractor Worker with batch size {settings.batch_size} "
        f"and interval {settings.interval_seconds} seconds."
    )

    while True:
        async with get_async_session() as session:
            batch = await get_batch(session, settings.batch_size)
            if batch:
                logger.info(f"Dispatching job offers with ids {[job_offer.id for job_offer in batch]}.")
                tasks = [handle_job_offer(job_offer, session) for job_offer in batch]
                await asyncio.gather(*tasks)
                await session.commit()

        await asyncio.sleep(settings.interval_seconds)
