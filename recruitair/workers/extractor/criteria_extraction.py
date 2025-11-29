from typing import List

from aiohttp import ClientSession, ClientTimeout
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.models import Criterion, JobOffer, JobOfferStatus
from . import logger, settings


class CriteriaExtractionResponse(BaseModel):
    class CriteriaItem(BaseModel):
        description: str = Field(..., description="Description of the extracted criterion from the job offer")
        importance: float = Field(
            ..., description="Importance of the extracted criterion on a scale from 0 to 1", ge=0, le=1
        )

    criteria: List[CriteriaItem]


async def extract_criteria(job_offer: JobOffer, session: AsyncSession) -> None:
    async with ClientSession(
        str(settings.extractor_api_base_url),
        headers={"Authorization": f"Bearer {settings.extractor_api_bearer_token}"},
        timeout=ClientTimeout(settings.http_timeout),
    ) as http_client:
        async with http_client.post(
            "/eval",
            json={"offer_text": job_offer.text},
        ) as response:
            response.raise_for_status()
            logger.info(f"Successfully extracted criteria for job offer id {job_offer.id}.")

            response_data = await response.json()
            criteria_response = CriteriaExtractionResponse.model_validate(response_data)
            for criterion in criteria_response.criteria:
                new_criterion = Criterion(
                    offer_id=job_offer.id,
                    description=criterion.description,
                    importance=criterion.importance,
                )
                session.add(new_criterion)
            job_offer.status = JobOfferStatus.DONE
