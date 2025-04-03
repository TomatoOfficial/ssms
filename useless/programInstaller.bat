pyinstaller -F program.py
del program.exe
copy dist\program.exe C:\Users\Administrator\Desktop\program
rmdir /s /q build
rmdir /s /q dist
del program.spec
