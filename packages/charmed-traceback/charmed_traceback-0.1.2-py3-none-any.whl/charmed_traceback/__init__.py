from .charmed_traceback import add_hook, Charmify

"""
# Example Usage
# Using a method such as this ensures that this Library isn't a strict dependency and can gently be removed,
# or only present as a developer dependency.

import contextlib

def dev_charm_traceback_handler() -> None:
    with contextlib.suppress(ImportError):
        import charmed_traceback.auto

dev_charm_traceback_handler()

def test_to_failure():
    while True:
        raise FileNotFoundError


test_to_failure()
"""