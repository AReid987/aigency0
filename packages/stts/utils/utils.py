import numpy as np


def next_power_of_2(x):
    """
    Calculates the next power of 2 greater than or equal to the given number.

    Args:
        x (int): The input number.

    Returns:
        int: The smallest power of 2 greater than or equal to x.
    """ return 1 if x == 0 else 2 ** (x - 1).bit_length()


def int2float(sound):
    """
    Taken from https://github.com/snakers4/silero-vad
    """

    abs_max = np.abs(sound).max()
    sound = sound.astype("float32")
    if abs_max > 0:
        sound *= 1 / 32768
    sound = sound.squeeze()  # depends on the use case
    return sound
