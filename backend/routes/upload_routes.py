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

from backend.services.parser_service import (
    parse_decompiled_file,
)

from backend.services.filter_service import (
    filter_functions,
    generate_filtered_code,
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

    functions = parse_decompiled_file(decompiled_output)

    # testing parser service
    # print(f"Parsed {len(functions)} functions")

    # for function in functions[:5]:
    #     print(function.name)

    filtered_functions = filter_functions(functions)

    # testing filtered functions
    for func in filtered_functions:
        print(func.name)

    filtered_code = generate_filtered_code(filtered_functions)

    print(f"Filtered down to {len(filtered_functions)} functions")

    return {
        "message": "Upload successful",
        "filename": file.filename,
        "saved_to": saved_path,
        "decompiled_output": decompiled_output,
        "total_functions": len(functions),
        "filtered_functions": len(filtered_functions),
        "filtered_code": filtered_code,
    }
