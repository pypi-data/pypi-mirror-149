# Import python libs
import subprocess


def all(hub):
    """
    clean everything up
    """
    subprocess.run("python3 setup.py clean", shell=True)
    subprocess.run("rm -rf build dist", shell=True)
