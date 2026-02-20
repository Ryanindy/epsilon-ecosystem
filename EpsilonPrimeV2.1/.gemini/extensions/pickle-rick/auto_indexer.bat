@echo off
pushd "%~dp0"
"C:\Users\Media Server\AppData\Local\Programs\Python\Python313\python.exe" scripts\auto_indexer.py %*
popd
