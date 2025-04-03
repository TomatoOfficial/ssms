pyinstaller -F ssms_v1.2.6.py
del ssms_v1.2.6.exe
copy dist\ssms_v1.2.6.exe C:\Users\OMEN\Desktop
rmdir /s /q build
rmdir /s /q dist
del ssms_v1.2.6.spec
