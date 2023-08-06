import os


CLI_CONFIG = {
    "ver": {"positional": True},
    "skip": {
        "nargs": "*",
        "choices": [
            "coerce",
            "version",
            "test",
            "git",
            "commit",
            "tag",
            "clean",
            "build",
            "input",
            "release",
            "push",
        ],
    },
    "remote": {},
    "root": {},
    "acct_file": {"source": "acct"},
    "acct_key": {"source": "acct"},
    "acct_profile": {"source": "idem"},
}
CONFIG = {
    "ver": {
        "help": "The semantic version number to apply to the release",
        "default": None,
    },
    "skip": {
        "help": "Skip phases with the given names in the release process",
        "default": None,
    },
    "remote": {
        "help": "The git remote to use when pushing a release",
        "default": "origin",
    },
    "root": {
        "help": "The path to the root of the project that will be released",
        "default": os.getcwd(),
    },
}
DYNE = {
    "pop_release": ["pop_release"],
    "exec": ["exec"],
    "acct": ["acct"],
}
