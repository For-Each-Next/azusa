"""Install the newest local wheel of the given packages."""

from __future__ import annotations

import logging
import subprocess  # noqa: S404
from pathlib import Path
from time import perf_counter_ns
from typing import TYPE_CHECKING

from packaging.utils import parse_wheel_filename

if TYPE_CHECKING:
    from os import PathLike

DEFAULT_FOLDER = "."
PACKAGE_NAME = "azusa"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def get_wheels(path: Path, pkg: str) -> list[Path]:
    """Return paths to matching wheel files sorted by version.

    Args:
        path: Directory in which to search for wheel files.
        pkg: Package name to match.

    Returns:
        A list of matching wheel file paths in ascending version order.
    """
    wheels = list(path.glob(f"{pkg}-*-py3-none-any.whl"))
    wheels.sort(key=lambda x: parse_wheel_filename(x.name)[1])
    return wheels


def install_wheel(
    path: Path,
    pkg: str,
    *,
    remove_old: bool,
) -> None:
    """Install the newest wheel and optionally remove older wheel files.

    Args:
        path: Directory containing the wheel files to consider.
        pkg: Package name to install.
        remove_old: If True, delete any older wheel files after
            installing the newest one.
    """
    logger = logging.getLogger(__name__)
    wheels = get_wheels(path, pkg)
    try:
        latest_wheel = wheels.pop()
    except IndexError:
        logger.warning("no wheels found")
        return
    subprocess.run(("pip", "install", latest_wheel), check=True)  # noqa: S603
    logger.info("installed %s", latest_wheel.name)
    if remove_old:
        for wheel in wheels:
            wheel.unlink()
            logger.info("removed %s", wheel.name)


def main(
    folder: PathLike[str] | str = DEFAULT_FOLDER,
    pkg: str = PACKAGE_NAME,
    *,
    remove_old: bool = True,
) -> None:
    """Install the newest wheel found in the specified folder.

    Args:
        folder: Directory that contains the wheel files to scan.
        pkg: Package name to install.
        remove_old: If True, remove older wheels after installation.
    """
    t0 = perf_counter_ns()
    logger = logging.getLogger(__name__)
    logger.info("starting wheel installation")
    install_wheel(Path(folder), pkg, remove_old=remove_old)
    logger.info("finished in %.1f ms", (perf_counter_ns() - t0) / 10**6)


if __name__ == "__main__":
    main()
