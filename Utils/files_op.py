import os


def create_dir_if_notexist(path):
    path_dir_name = os.path.dirname(path)
    if not os.path.exists(path_dir_name):
        os.mkdir(path)
        print(f"[+] Directory created at : [{path_dir_name}]")


def convertToBinaryData(filename):
    """Convert digital data to binary format"""

    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData
