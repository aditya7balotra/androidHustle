import re

def split_line(line):
    """
    This splits the line only on commas
    that are followed by a word and an = sign
    """
    parts = re.split(r',\s*(?=\w+=)', line)
    return parts

def validate_int(value):
    try:
        int(value)
        return True
    except Exception as e:
        return False
    
def check_package(packageUri, device):
    """
    Params:
        packageUri: the package URI
        device: the adb device object
    Returns:
        Ture  | if installed
        False | if not found
    """

    return device.shell(f"pm path {packageUri}").strip().startswith("package:")

    