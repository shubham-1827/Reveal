import re

from backend.models.function_model import (
    DecompiledFunction,
)


def generate_call_graph(
    functions: list[DecompiledFunction],
) -> dict:

    function_names = {function.name for function in functions}
    nodes = []
    edges = []
    added_edges = set()

    for function in functions:
        nodes.append(
            {
                "id": function.name,
                "label": function.name,
            }
        )

        for name in function_names:
            if name == function.name:
                continue
            pattern = rf"\b{re.escape(name)}\s*\("

            if re.search(pattern, function.code):
                edge_key = (
                    function.name,
                    name,
                )

                if edge_key in added_edges:
                    continue

                added_edges.add(edge_key)

                edges.append(
                    {
                        "from": function.name,
                        "to": name,
                    }
                )

    return {
        "nodes": nodes,
        "edges": edges,
    }
