from backend.services.parser_service import (
    parse_decompiled_file,
)

functions = parse_decompiled_file("outputs/test_decompiled.c")

print(f"Total functions: {len(functions)}")
print()

for function in functions:
    print("NAME:", function.name)
    print("ADDRESS:", function.address)

    print("CODE:")
    print(function.code[:200])

    print("-" * 50)
