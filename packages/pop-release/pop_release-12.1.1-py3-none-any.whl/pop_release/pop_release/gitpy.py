from git import Remote
from git import Repo

__virtualname__ = "git"


def commit(hub, git_root: str, version: str):
    """
    Commit the given changes to git
    """
    repo = Repo(git_root, search_parent_directories=True)
    repo.git.add(update=True)
    repo.index.commit(f'"Version bump to {version}"')


def tag(hub, git_root: str, version: str):
    """
    Set the tag
    """
    repo = Repo(git_root, search_parent_directories=True)
    repo.create_tag(f"v{version}", ref="HEAD", message=f"Version {version}", force=True)


def push(hub, git_root: str, remote: str = "origin"):
    """
    Push the changes
    """
    repo = Repo(git_root, search_parent_directories=True)
    origin: Remote = repo.remotes[remote]
    origin.fetch()
    origin.push(repo.active_branch.name)
