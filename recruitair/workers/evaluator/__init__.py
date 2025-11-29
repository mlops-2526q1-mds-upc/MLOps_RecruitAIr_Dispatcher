import asyncio
import logging
import traceback
from typing import Sequence, Tuple

from sqlalchemy import exists, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from .evaluator_settings import EvaluatorWorkerSettings

logger = logging.getLogger(__name__)
settings = EvaluatorWorkerSettings()

from ...database import get_async_session
from ...database.models import Applicant, ApplicantScore, Criterion
from .applicant_evaluation import evaluate_applicant


async def get_batch(session: AsyncSession, batch_size: int) -> Sequence[Tuple[Applicant, Criterion]]:
    query = (
        select(Applicant, Criterion)
        .join(Criterion, Applicant.offer_id == Criterion.offer_id)
        .where(
            ~exists().where(
                (ApplicantScore.applicant_id == Applicant.id) & (Criterion.id == ApplicantScore.criteria_id)
            )
        )
        .order_by(Applicant.created_at)
    )
    offset = 0
    batch = []
    while len(batch) < batch_size:
        result = await session.execute(query.offset(offset))
        candidate_row = result.first()
        if not candidate_row:
            break
        offset += 1
        applicant, criterion = candidate_row
        # Before adding it to the batch, attempt locking the combination of Applicant and Criterion to avoid race
        # conditions with other worker instances. If the lock cannot be acquired, skip this candidate.
        lock_acquired = await session.execute(
            text("SELECT pg_try_advisory_xact_lock(:lock_key)").bindparams(lock_key=hash((applicant.id, criterion.id)))
        )
        if lock_acquired.scalar():
            batch.append((session, (applicant, criterion)))
    return batch


async def handle_applicant_score(applicant: Applicant, criterion: Criterion, session: AsyncSession):
    try:
        await evaluate_applicant(applicant, criterion, session)
    except Exception as e:
        logger.error(f"Error processing applicant id {applicant.id} and criterion id {criterion.id}: {e}")
        logger.error("Stack trace:")
        for line in traceback.format_exception(type(e), e, e.__traceback__):
            logger.error(line)


async def evaluator_worker():
    logger.info(
        f"Starting Evaluator Worker with batch size {settings.batch_size} "
        f"and interval {settings.interval_seconds} seconds."
    )

    while True:
        async with get_async_session() as session:
            batch = await get_batch(session, settings.batch_size)
            if batch:
                logger.info(
                    f"Dispatching applicant and criterion pairs {', '.join(f'(a:{applicant.id}, c:{criterion.id})' for applicant, criterion in batch)}."
                )
                tasks = [handle_applicant_score(applicant, criterion, session) for (applicant, criterion) in batch]
                await asyncio.gather(*tasks)
                await session.commit()

            await asyncio.sleep(settings.interval_seconds)
