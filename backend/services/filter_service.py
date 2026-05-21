from backend.services.parser_service import (
    DecompiledFunction,
)

BLACKLIST = {
    "pre_c_init",
    "pre_cpp_init",
    "WinMainCRTStartup",
    "mainCRTStartup",
    "atexit",
    "printf",
    "mark_section_writable",
    "dtoa_lock",
    "dtoa_lock_cleanup",
    "strnlen",
    "wcsnlen",
    "mingw_get_invalid_parameter_handler",
    "mingw_set_invalid_parameter_handler",
    "wcrtomb",
    "wcsrtombs",
    "mbrtowc",
    "mbsrtowcs",
    "mbrlen",
    "abort",
    "calloc",
    "exit",
    "fprintf",
    "fputc",
    "free",
    "fwrite",
    "localeconv",
    "malloc",
    "memcpy",
    "memset",
    "signal",
    "strerror",
    "strlen",
    "strncmp",
    "vfprintf",
    "wcslen",
    "WideCharToMultiByte",
    "VirtualQuery",
    "VirtualProtect",
    "TlsGetValue",
    "Sleep",
    "SetUnhandledExceptionFilter",
    "MultiByteToWideChar",
    "LeaveCriticalSection",
    "IsDBCSLeadByteEx",
    "InitializeCriticalSection",
    "GetLastError",
    "EnterCriticalSection",
    "DeleteCriticalSection",
    ".text",
}

PREFIXES = [
    "__",
    "_",
]


def should_filter(
    function_name: str,
) -> bool:

    if function_name in BLACKLIST:
        return True

    for prefix in PREFIXES:

        if function_name.startswith(prefix):
            return True

    return False


def filter_functions(
    functions: list[DecompiledFunction],
) -> list[DecompiledFunction]:

    filtered = []

    for function in functions:

        if should_filter(function.name):
            continue

        filtered.append(function)

    return filtered


def generate_filtered_code(
    functions: list[DecompiledFunction],
) -> str:

    headers = [
        "#include <stdio.h>",
        "#include <stdlib.h>",
        "#include <stdint.h>",
    ]

    output = "\n".join(headers)
    output += "\n\n"

    for function in functions:

        output += f"/* Function: {function.name} " f"@ 0x{function.address} */\n\n"

        output += function.code
        output += "\n\n"

    return output
