import io
from typing import List

import twine.commands.check as tw_check
import twine.commands.register as tw_register
import twine.commands.upload as tw_upload

__virtualname__ = "cmd"


__contracts__ = ["soft_fail"]


async def check(hub, dists: List[str], strict: bool = False):
    """
    Verify the named distribution files
    :param hub:
    :param dists:
    :param strict:
    """
    if isinstance(dists, str):
        dists = dists.split()
    with io.StringIO() as output:
        failure = tw_check.check(dists=dists, strict=strict, output_stream=output)

        ret = output.getvalue()

        return {"result": not failure, "ret": ret, "comment": failure}


async def register(hub, ctx, package: str):
    """
    Register a package name with PyPi

    :param hub:
    :param ctx:
    :param package:
    """
    with io.StringIO() as output:
        failure = tw_register.register(
            register_settings=ctx.acct.settings, package=package
        )
        ret = output.getvalue()

        return {"result": not failure, "ret": ret, "comment": failure}


async def upload(hub, ctx, dists: List[str] or str):
    if isinstance(dists, str):
        dists = dists.split()

    with io.StringIO() as output:
        failure = tw_upload.upload(upload_settings=ctx.acct.settings, dists=dists)

        ret = output.getvalue()

        return {"result": not failure, "ret": ret, "comment": failure}
