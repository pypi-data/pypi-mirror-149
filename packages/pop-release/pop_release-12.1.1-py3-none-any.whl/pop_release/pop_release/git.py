# Import python libs
import subprocess


def commit(hub):
    """
    Commit the given changes to git
    """
    ver = hub.OPT["pop_release"]["ver"]
    subprocess.run(f'git commit -a -m "Version bump to {ver}"', shell=True)


def tag(hub):
    """
    Set the tag
    """
    ver = hub.OPT["pop_release"]["ver"]
    subprocess.run(f'git tag -a v{ver} -m "Version {ver}"', shell=True)


def push(hub):
    """
    Push the changes
    """
    subprocess.run(f"git push", shell=True)
    subprocess.run(f"git push --tags", shell=True)
