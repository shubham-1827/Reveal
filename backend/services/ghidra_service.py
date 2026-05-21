from pathlib import Path
import shutil
import subprocess
import uuid
import os

# GHIDRA_HOME = Path("/opt/ghidra")
GHIDRA_HOME = Path(
    os.getenv(
        "GHIDRA_HOME",
        "/opt/ghidra",
    )
)

GHIDRA_HEADLESS = GHIDRA_HOME / "support" / "analyzeHeadless"

if not GHIDRA_HOME.exists():
    raise RuntimeError("Invalid GHIDRA_HOME path")

if not GHIDRA_HEADLESS.exists():
    raise RuntimeError("analyzeHeadless not found")

PROJECTS_DIR = Path("temp")
OUTPUTS_DIR = Path("outputs")

GHIDRA_SCRIPT_DIR = Path("backend/ghidra_scripts")

DECOMP_TIMEOUT = 300


def run_ghidra_analysis(
    executable_path: str,
) -> str:

    executable = Path(executable_path)

    project_name = f"reveal_{uuid.uuid4().hex}"

    project_dir = PROJECTS_DIR / project_name

    output_file = OUTPUTS_DIR / f"{executable.stem}_decompiled.c"

    project_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    command = [
        str(GHIDRA_HEADLESS),
        str(project_dir),
        project_name,
        "-import",
        str(executable),
        "-postScript",
        "export_decomp.py",
        str(output_file),
        "-scriptPath",
        str(GHIDRA_SCRIPT_DIR),
        "-deleteProject",
    ]

    try:
        subprocess.run(
            command,
            check=True,
            timeout=DECOMP_TIMEOUT,
        )

    except subprocess.TimeoutExpired:
        raise RuntimeError("Ghidra analysis timed out")

    except subprocess.CalledProcessError:
        raise RuntimeError("Ghidra analysis failed")

    finally:
        if project_dir.exists():
            shutil.rmtree(
                project_dir,
                ignore_errors=True,
            )

    return str(output_file)
