# Import python libs
import subprocess


def build(hub):
    """
    Build the release
    """
    subprocess.run("python3 setup.py sdist bdist_wheel", shell=True)


def push(hub):
    """
    Push the build up to pypi!
    """
    subprocess.run("twine upload dist/*", shell=True)
