from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from backend.services.upload_service import (
    save_upload,
    validate_extension,
    validate_file_size,
)

from backend.services.ghidra_service import (
    run_ghidra_analysis,
)

router = APIRouter()


@router.post("/upload")
async def upload_executable(
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Missing filename",
        )

    if not validate_extension(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Only .exe files are allowed",
        )

    is_valid_size = await validate_file_size(file)

    if not is_valid_size:
        raise HTTPException(
            status_code=400,
            detail="File exceeds size limit",
        )

    saved_path = await save_upload(file)

    decompiled_output = run_ghidra_analysis(saved_path)

    return {
        "message": "Upload successful",
        "filename": file.filename,
        "saved_to": saved_path,
        "decompiled_output": decompiled_output,
    }
