from pydantic import BaseModel

from fastapi import (
    APIRouter,
    HTTPException,
)

from backend.services.ai_service import (
    explain_function,
)

router = APIRouter()


class ExplainRequest(BaseModel):
    function_name: str
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
