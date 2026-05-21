# @author REVEAL
# @category REVEAL

from ghidra.app.decompiler import (
    DecompInterface,
)

from ghidra.util.task import (
    ConsoleTaskMonitor,
)

import os


output_path = getScriptArgs()[0]

monitor = ConsoleTaskMonitor()

decompiler = DecompInterface()
decompiler.openProgram(currentProgram)

functions = currentProgram.getFunctionManager()

with open(output_path, "w") as output_file:

    for function in functions.getFunctions(True):

        result = decompiler.decompileFunction(
            function,
            60,
            monitor,
        )

        decompiled = result.getDecompiledFunction()

        if not decompiled:
            continue

        function_code = decompiled.getC()

        function_name = function.getName()

        address = function.getEntryPoint().toString()

        output_file.write("/* Function: %s @ 0x%s */\n\n" % (function_name, address))

        output_file.write(function_code)

        output_file.write("\n\n")
