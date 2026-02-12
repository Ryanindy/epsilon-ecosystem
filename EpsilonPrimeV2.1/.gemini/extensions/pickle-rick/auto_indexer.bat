@echo off
pushd "%~dp0"
python scripts\auto_indexer.py %*
popd