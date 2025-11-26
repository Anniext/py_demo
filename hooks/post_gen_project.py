"""Post gen hook for uv-based projects.

This hook cleans up legacy dependency management files (pip, pipenv, etc.)
so that the generated project uses only uv with pyproject.toml / uv.lock.
It also performs some basic initialization for local development.
"""
import logging
import os
import shutil
import subprocess
import sys

_logger = logging.getLogger(__name__)


LEGACY_DEP_FILES = [
    "requirements.txt",
    "requirements-dev.txt",
    "requirements",
    "Pipfile",
    "Pipfile.lock",
    "poetry.lock",
    "poetry.toml",
    "environment.yml",
]


def clean_extra_package_management_files():
    """Remove legacy dependency management files and optional Heroku files.

    The template is uv-first, keeping ``pyproject.toml`` and ``uv.lock`` as
    the single source of dependency management.
    """

    use_heroku = "{{cookiecutter.use_heroku}}"
    to_delete = list(LEGACY_DEP_FILES)

    if use_heroku == "False":
        to_delete.extend(["Procfile", "app.json"])

    try:
        for file_or_dir in to_delete:
            if os.path.isfile(file_or_dir):
                os.remove(file_or_dir)
            elif os.path.isdir(file_or_dir):
                shutil.rmtree(file_or_dir)

        if os.path.isfile(".env.example") and not os.path.isfile(".env"):
            shutil.copy(".env.example", ".env")

        # Initialize a local dev database file if needed
        open("dev.db", "a").close()
    except OSError as e:
        _logger.warning(
            "While attempting to remove or initialize file(s) an error occurred"
        )
        _logger.warning(f"Error: {e}")
        sys.exit(1)


def setup_uv_environment():
    """Ensure uv dependencies are installed and print next-step hints.

    This will:
    - Check whether ``uv`` is available on PATH.
    - If available, run ``uv sync`` once to install project dependencies.
    - Log helpful next-step commands for the user.
    """

    uv_executable = shutil.which("uv")
    if uv_executable is None:
        _logger.warning(
            "uv is not installed or not found on PATH. "
            "Please install uv from https://github.com/astral-sh/uv "
            "and run `uv sync` manually."
        )
        return

    _logger.info("Detected uv executable at %s", uv_executable)
    _logger.info("Running `uv sync` to install project dependencies...")

    try:
        result = subprocess.run(
            [uv_executable, "sync"],
            check=False,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        if result.returncode != 0:
            _logger.warning(
                "uv sync exited with non-zero status (%s). "
                "You may need to run `uv sync` manually.",
                result.returncode,
            )
        else:
            _logger.info(
                "uv sync completed successfully. "
                "You can start developing with commands like:\n"
                "  uv run python -m src\n"
                "  uv run pytest"
            )
    except OSError as e:
        _logger.warning("Failed to execute uv: %s", e)
        _logger.warning("Please run `uv sync` manually after installation.")


if __name__ == "__main__":
    clean_extra_package_management_files()
    setup_uv_environment()
