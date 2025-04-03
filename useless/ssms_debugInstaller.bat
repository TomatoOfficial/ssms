pyinstaller -F ssms_debug.py
del ssms_debug.exe
copy dist\ssms_debug.exe C:\Users\Administrator\Desktop\ssms
rmdir /s /q build
rmdir /s /q dist
del ssms_debug.spec
