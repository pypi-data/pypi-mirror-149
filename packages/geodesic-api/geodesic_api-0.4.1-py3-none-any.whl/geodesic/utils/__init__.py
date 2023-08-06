import datetime
import pytz


def is_offset_aware(t: datetime.datetime):
    '''
    Returns True if input is offset aware, False otherwise
    '''
    if t.tzinfo is not None and t.tzinfo.utcoffset(t) is not None:
        return True
    return False


def datetime_to_utc(d: datetime.datetime):
    '''
    Ensures input is localized UTC
    '''

    if is_offset_aware(d):
        return d.astimezone(pytz.UTC)

    return pytz.UTC.localize(d)


class MockImport:
    """
    Use a MockImport when something requires a particular module. On import error,
    set the module instance to this class initialized with the import module name.
    This will raise a readable exception when used instead of a more challenging error.
    """
    def __init__(self, module_name: str):
        self.module_name = module_name

    def __getattr__(self, attr):
        if attr not in self.__dict__:
            raise ImportError(f"'{self.module_name}' must be installed in order to use this function")
        else:
            return super().__getattribute__(attr)
