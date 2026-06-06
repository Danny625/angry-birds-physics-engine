@echo off
set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
.\.venv\Scripts\python.exe -m pytest tests -p no:cacheprovider --disable-warnings --color=no
