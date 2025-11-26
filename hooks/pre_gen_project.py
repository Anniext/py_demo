import logging
import sys

logging.basicConfig()
_logger = logging.getLogger(__name__)


def check_python_version():
    python_major_version = sys.version_info[0]
    python_minor_version = sys.version_info[1]
    # Must remain compatible with Python 2 to provide useful error message.
    warning = (
        "\nWARNING: You are running cookiecutter using "
        "Python {}.{}, but a version >= Python 3.11+ is required.\n"
        "Either install a more recent version of Python, or use the Docker instructions.\n"
    ).format(python_major_version, python_minor_version)
    if (python_major_version == 2) or (
        python_major_version == 3 and python_minor_version < 7
    ):
        _logger.warning(warning)
        sys.exit(1)


if __name__ == "__main__":
    check_python_version()
