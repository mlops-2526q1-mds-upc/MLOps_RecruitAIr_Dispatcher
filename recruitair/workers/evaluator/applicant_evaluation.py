from aiohttp import ClientSession, ClientTimeout
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.models import Applicant, ApplicantScore, Criterion
from . import logger, settings


class ApplicantEvaluationResponse(BaseModel):
    score: float = Field(
        ..., description="The overall score assigned to the applicant for the given criterion", ge=0, le=1
    )


async def evaluate_applicant(applicant: Applicant, criterion: Criterion, session: AsyncSession) -> None:
    async with ClientSession(
        str(settings.evaluator_api_base_url),
        headers={"Authorization": f"Bearer {settings.evaluator_api_bearer_token}"},
        timeout=ClientTimeout(settings.http_timeout),
    ) as http_client:
        async with http_client.post(
            "eval",
            json={"criteria_description": criterion.description, "applicant_cv": applicant.cv},
        ) as response:
            response.raise_for_status()
            logger.info(f"Successfully evaluated applicant id {applicant.id} for criterion id {criterion.id}.")

            response_data = await response.json()
            evaluation_response = ApplicantEvaluationResponse.model_validate(response_data)
            new_applicant_score = ApplicantScore(
                applicant_id=applicant.id,
                criteria_id=criterion.id,
                score=evaluation_response.score,
            )
            session.add(new_applicant_score)
