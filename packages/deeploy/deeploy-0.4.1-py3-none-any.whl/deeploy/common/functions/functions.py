import os
import shutil
import logging


def to_lower_camel(string: str) -> str:
    if string == 'public_url':
        return 'publicURL'

    camel_case = ''.join(word.capitalize() for word in string.split('_'))
    lower_camel_case = camel_case[0].lower() + camel_case[1:]
    return lower_camel_case


def delete_all_contents_in_directory(folder_path: str) -> None:
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logging.error('Failed to delete %s. Reason: %s' % (file_path, e))
    return


def directory_exists(folder_path: str) -> bool:
    return os.path.exists(folder_path)


def directory_empty(folder_path: str) -> bool:
    return len(os.listdir(folder_path)) == 0


def file_exists(file_path: str) -> bool:
    return os.path.isfile(file_path)
