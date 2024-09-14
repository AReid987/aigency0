import sys

from inputimeout import TimeoutOccurred, inputimeout

<< << << < HEAD
== == == =
>>>>>> > 83f71b59(new remote. who dis?)


def timeout_input(prompt, timeout=10):
    try:


<< << << < HEAD
        import readline
== == == =
        if sys.platform != "win32": import readline
>>>>>> > 83f71b59(new remote. who dis?)
        user_input = inputimeout(prompt=prompt, timeout=timeout)
        return user_input
    except TimeoutOccurred:
        return ""