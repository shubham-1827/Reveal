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

from backend.services.session_service import store_functions

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

    # # testing filtered functions
    # for func in filtered_functions:
    #     print(func.name)

    filtered_code = generate_filtered_code(filtered_functions)

    store_functions(filtered_functions)

    print(f"Filtered down to {len(filtered_functions)} functions")

    with open(
        decompiled_output,
        "r",
        encoding="utf-8",
    ) as output_file:

        raw_code = output_file.read()

    return {
        "message": "Upload successful",
        "filename": file.filename,
        "raw_code": raw_code,
        "filtered_code": filtered_code,
        "total_functions": len(functions),
        "filtered_functions": len(filtered_functions),
        "functions": [
            {
                "name": func.name,
                "address": func.address,
                "code": func.code,
            }
            for func in filtered_functions
        ],
    }
