from cx_Freeze import setup, Executable

setup(
    name = "Play Snake",
    options = {'build_exe':{'packages':['pygame']}},
    executables = [Executable(r"D:\play-snake-master\main.py")]
)