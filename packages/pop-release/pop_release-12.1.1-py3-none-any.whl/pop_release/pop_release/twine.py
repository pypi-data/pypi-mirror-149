import pathlib


async def push(hub, ctx, root_path: pathlib.Path):
    """
    Push the build up to pypi!
    """
    ret = await hub.exec.twine.cmd.check(str(root_path / "dist" / "*"))
    if not ret.result:
        raise RuntimeError(f"Dist files failed check:\n{ret.ret}")

    ret = await hub.exec.twine.cmd.upload(ctx, str(root_path / "dist" / "*"))
    if not ret.result:
        raise RuntimeError(f"Dist files failed to upload:\n{ret.ret}")
