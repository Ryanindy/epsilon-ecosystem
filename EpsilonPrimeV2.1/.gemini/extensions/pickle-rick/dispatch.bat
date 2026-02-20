@echo off
pushd "%~dp0"
"C:\Users\Media Server\AppData\Local\Programs\Python\Python313\python.exe" scripts\dispatch_hook_fast.py %*
popd
