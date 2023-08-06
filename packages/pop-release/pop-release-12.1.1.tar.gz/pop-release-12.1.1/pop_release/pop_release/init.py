import pathlib
from typing import List

import semantic_version


def __init__(hub):
    hub.pop.sub.add(dyne_name="idem")


def cli(hub):
    hub.pop.config.load(["pop_release", "idem", "acct"], cli="pop_release")

    print(hub.OPT.acct)
    hub.pop.loop.create()
    hub.pop.Loop.run_until_complete(
        hub.pop_release.init.run(
            root_path=pathlib.Path(hub.OPT.pop_release.root),
            version=hub.OPT.pop_release.ver,
            skip=hub.OPT.pop_release.skip,
            remote=hub.OPT.pop_release.remote,
            acct_file=hub.OPT.acct.acct_file,
            acct_key=hub.OPT.acct.acct_key,
            acct_profile=hub.OPT.idem.acct_profile,
        )
    )


async def run(
    hub,
    version,
    root_path: pathlib.Path,
    skip: List[str],
    remote: str,
    acct_file: str,
    acct_key: str,
    acct_profile: str,
):
    if skip is None:
        print("Running full release process")
        skip = []
    print(f"Working directory: {root_path}")
    print("Generating ctx")
    ctx = await hub.idem.acct.ctx(
        "exec.twine.",
        acct_file=acct_file,
        acct_key=acct_key,
        acct_profile=acct_profile,
    )
    if "coerce" not in skip:
        print("Coercing the version number to semantic style")
        version = str(semantic_version.Version.coerce(str(version)))
    if "version" not in skip:
        print("Updating release version")
        hub.pop_release.version.set_ver(root_path, version)
        print("Updating docs version")
        hub.pop_release.version.set_doc(root_path, version)
    if "test" not in skip:
        print("Running tests")
        hub.pop_release.test.pytest(root_path)
    if "commit" not in skip and "git" not in skip:
        print("Committing changes")
        hub.pop_release.git.commit(root_path, version)
    if "tag" not in skip and "git" not in skip:
        print("Tagging commit")
        hub.pop_release.git.tag(root_path, version)
    if "clean" not in skip:
        print("Cleaning up")
        hub.pop_release.dist.clean(root_path)
    if "build" not in skip:
        print("Building dist files")
        hub.pop_release.dist.build(root_path)
    if "input" in skip:
        choice = "y"
    else:
        choice = input(
            f"Build for version {version} is complete, Push to git and pypi? [Y,n] "
        )
    if not choice or choice.lower().startswith("y"):
        if "release" not in skip:
            print("Releasing to repository")
            await hub.pop_release.twine.push(ctx, root_path)
        if "push" not in skip and "git" not in skip:
            print(f"Pushing to git remote: {remote}")
            hub.pop_release.git.push(root_path, remote)
    print("Success!")
