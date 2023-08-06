import pathlib

import pytest as test


def pytest(hub, root_dir: pathlib.Path):
    """
    Run pytest and fail the sequence if pytest fails
    """
    retcode = test.main([str(root_dir / "tests"), "--color=yes", "--quiet"])
    if retcode == 5:
        # No tests, skip
        hub.log.warning("This project has no tests")
        return
    if retcode:
        raise ChildProcessError(f"Pytest failed: {retcode}")
