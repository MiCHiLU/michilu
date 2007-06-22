import os.path
import imp

def get_optional_settings(optional_settings=None):
    _optional_settings = optional_settings or "conf/settings/settings_overload.py"
    dir_name = os.path.dirname(_optional_settings)
    file_name = os.path.basename(_optional_settings).split(".")[0]
    _settings = None
    result = {}
    try:
        f, fn, desc = imp.find_module(file_name, [dir_name])
        _settings = imp.load_module(file_name, f, fn, desc)
    except ImportError:
        pass
    if _settings:
        for key in _settings.__dict__.keys():
            if not key[0].startswith("_"):
                result[key] = _settings.__dict__[key]
    return result
