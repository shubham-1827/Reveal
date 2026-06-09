from pydantic import BaseModel

from fastapi import (
    APIRouter,
    HTTPException,
)

from backend.services.ai_service import (
    explain_function,
)

from backend.services.summary_service import (
    generate_summary,
)

from backend.services.polish_service import (
    polish_code,
)

from backend.models.function_model import (
    DecompiledFunction,
)

router = APIRouter()


class ExplainRequest(BaseModel):
    function_name: str
    code: str


class SummaryRequest(BaseModel):
    functions: list[DecompiledFunction]


class PolishRequest(BaseModel):
    code: str


@router.post("/explain")
async def explain(
    request: ExplainRequest,
):

    try:

        explanation = explain_function(
            request.function_name,
            request.code,
        )

        return {
            "explanation": explanation,
        }

    except RuntimeError as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


@router.post("/summary")
async def summary(
    request: SummaryRequest,
):

    try:

        summary = generate_summary(
            request.functions,
        )

        return {
            "summary": summary,
        }

    except RuntimeError as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ai se polished output ke liye hai yeh endpoint
@router.post("/polish")
async def polish(
    request: PolishRequest,
):

    try:

        polished_code = polish_code(
            request.code,
        )

        return {
            "polished_code": polished_code,
        }

    except RuntimeError as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )
