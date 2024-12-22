@echo off
call uv pip uninstall st_client
call rm -R build
uv pip install .