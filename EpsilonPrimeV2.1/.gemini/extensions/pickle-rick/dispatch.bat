@echo off
pushd "%~dp0"
python scripts\dispatch_hook.py %*
popd