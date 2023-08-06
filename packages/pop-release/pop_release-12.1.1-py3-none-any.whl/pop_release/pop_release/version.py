import glob
import pathlib


def set_doc(hub, root_dir: pathlib.Path, version: str):
    """
    Set the version on the docs
    """
    lines = []
    paths = [root_dir / "docs" / "conf.py", root_dir / "docs" / "source" / "conf.py"]
    path = None
    for check in paths:
        if check.exists():
            path = check
            break
    else:
        hub.log.warning(
            "No docs set up for this project, use 'pop-create docs' to set up docs"
        )
        return
    with path.open("r") as rfh:
        for line in rfh.readlines():
            if line.startswith("ver"):
                lines.append(f'version = "{version}"\n')
                continue
            elif line.startswith("release"):
                lines.append(f'release = "{version}"\n')
                continue
            else:
                lines.append(line)
    with path.open("w+") as wfh:
        wfh.writelines(lines)


def set_ver(hub, root_dir: pathlib.Path, version: str):
    """
    Set the version to the <project name>/version.py
    """
    ver_str = f'version = "{version}"\n'
    path = root_dir / "version.py"

    if not path.exists():
        # try and find the path from a relative path
        paths = glob.glob(str(root_dir / "*" / "version.py"))

        if paths:
            path = pathlib.Path(paths[0])

    if path.exists():
        with path.open("w+") as wfh:
            wfh.write(ver_str)
