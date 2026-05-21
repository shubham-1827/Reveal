from fastapi import APIRouter, HTTPException

from backend.services.session_service import (
    get_function_by_name,
    get_functions,
)

router = APIRouter()


@router.get("/functions")
async def fetch_functions():

    functions = get_functions()

    if not functions:
        return {
            "functions": [],
        }

    return {
        "functions": [
            {
                "name": function.name,
                "address": function.address,
            }
            for function in functions
        ]
    }


@router.get("/function/{name}")
async def fetch_function(name: str):

    function = get_function_by_name(name)

    if not function:
        raise HTTPException(
            status_code=404,
            detail="Function not found",
        )

    return {
        "name": function.name,
        "address": function.address,
        "code": function.code,
    }
