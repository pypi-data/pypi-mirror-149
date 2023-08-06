import os

import twine.settings as settings


def gather(hub, profiles):
    sub_profiles = {hub.acct.BACKEND_KEY: {"twine_pypirc": {}}}
    for name, ctx in profiles.get("twine", {}).items():
        sub_profiles[name] = {
            "settings": settings.Settings(non_interactive=True, **ctx)
        }
    return sub_profiles


def default(hub):
    """
    A default profile to use if no encrypted credentials were found
    """
    return {
        "settings": settings.Settings(
            non_interactive=True,
            config_file=os.path.expanduser("~/.pypirc"),
        )
    }
