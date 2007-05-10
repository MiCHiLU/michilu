import os.path


_proj_path = "/path-to/michilu/"
_proj_name = "michilu"
if DEBUG:
    _proj_path = ""
    _proj_name = os.path.split(os.path.abspath(""))[-1]
_proj_db = os.path.abspath('%s../db/%s.db' % (PROJECT_PATH, _proj_name))

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = _proj_db

SECRET_KEY = ''
