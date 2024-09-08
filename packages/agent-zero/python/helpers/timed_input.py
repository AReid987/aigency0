<<<<<<< HEAD
=======
import sys
>>>>>>> 83f71b59 (new remote. who dis?)
from inputimeout import inputimeout, TimeoutOccurred

def timeout_input(prompt, timeout=10):
    try:
<<<<<<< HEAD
        import readline
=======
        if sys.platform != "win32": import readline
>>>>>>> 83f71b59 (new remote. who dis?)
        user_input = inputimeout(prompt=prompt, timeout=timeout)
        return user_input
    except TimeoutOccurred:
        return ""