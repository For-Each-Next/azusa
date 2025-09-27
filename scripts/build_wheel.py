"""Build wheel with UTC-timestamped versioning and remove older ones."""

import datetime
import logging
import re
import subprocess  # noqa: S404
from os import PathLike
from pathlib import Path
from time import perf_counter_ns

PACKAGE_NAME = "azusa"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def update_version(root_dir: Path) -> str:
    """Update `version` in `__metadata__` with the UTC timestamp.

    Args:
        root_dir: Path to the project root directory that contains
            pyproject.toml.

    Returns:
        The new version string in the form 'YYYY.M.D+tHHMMSS' (UTC).
    """
    # get timestamped version string
    dt = datetime.datetime.now(tz=datetime.UTC)
    version = f"{dt.year}.{dt.month}.{dt.day}+t{dt:%H%M%S}"
    # update version
    config_file = root_dir / "src" / PACKAGE_NAME / "__metadata__.py"
    source = config_file.read_text(encoding="utf-8")
    source = re.sub(
        r"^__version__\s*=\s*.+$",
        f'__version__ = "{version}"',
        source,
        flags=re.MULTILINE,
    )
    config_file.write_text(source, encoding="utf-8")
    # return the version string
    return version


def remove_old_wheels(root_dir: Path, version: str) -> None:
    """Remove wheel files in `dist` that do not match the given version.

    Args:
        root_dir: Path to the project root directory.
        version: The version string of the newly built wheel to retain.
    """
    logger = logging.getLogger(__name__)
    dist_dir = root_dir / "dist"
    new_wheel = dist_dir / f"{PACKAGE_NAME}-{version}-py3-none-any.whl"
    for wheel in dist_dir.glob(f"{PACKAGE_NAME}-*-py3-none-any.whl"):
        if not wheel.samefile(new_wheel):
            wheel.unlink()
            logger.info("removed old wheel %s", wheel.name)


def build_wheel(root_dir: Path, *, remove_old: bool) -> None:
    """Build the wheel with and prune older wheels.

    Args:
        root_dir: Path to the project root directory.
        remove_old: Whether to remove older wheel files.
    """
    logger = logging.getLogger(__name__)
    version = update_version(root_dir)
    subprocess.run(("uv", "build", "--wheel", root_dir), check=True)  # noqa: S603
    logger.info("built new wheel of version %s", version)
    if remove_old:
        remove_old_wheels(root_dir, version)


def main(root: PathLike[str] | str = ".", *, remove_old: bool = True) -> None:
    """Entry point for building a wheel from the given project root.

    Args:
        root: Path str to the project root directory.
        remove_old: Whether to remove older wheel files.
    """
    t0 = perf_counter_ns()
    logger = logging.getLogger(__name__)
    logger.info("starting wheel build")
    build_wheel(Path(root), remove_old=remove_old)
    logger.info("finished in %.1f ms", (perf_counter_ns() - t0) / 10**6)


if __name__ == "__main__":
    main()
