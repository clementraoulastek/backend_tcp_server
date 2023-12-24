"""Module for handling pictures"""


def return_default_pic() -> bytes:
    """
    Returns the default profile picture

    Returns:
        bytes: The default profile picture
    """
    path = "resources/pictures/default_av.png"
    return open(path, "rb").read()
