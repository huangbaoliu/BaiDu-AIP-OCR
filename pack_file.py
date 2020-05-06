import  os
if __name__ == '__main__':
    from PyInstaller.__main__ import run
    opts=['Text_recognition.py', '-w','-F',  '-i', "ahdms.ico", '--version-file', 'file_version.txt']
    run(opts)