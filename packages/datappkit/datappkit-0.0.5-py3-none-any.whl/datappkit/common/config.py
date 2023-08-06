import os

from datappkit.utils import file_utils


_t_filename = os.environ['HOME'] + os.sep + ".datapp-kit.session"
_token = ''


def debug():
    return os.getenv('DATAPP_KIT_DEBUG', 'off') == 'on'


def set_authorization(jwt):
    global _token
    _token = jwt
    return file_utils.write_file(_t_filename, jwt)


def authorization():
    global _token
    if not _token:
        _token = file_utils.read_file(_t_filename)
    return _token
