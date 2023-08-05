import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": {"common", "project_logging", "server"}
}
setup(
    name="mess_server",
    version="0.8.7",
    description="mess_server",
    options={
        "build_exe": build_exe_options
    },
    executables=[Executable('server_script.py',
                            base='Win32GUI',
                            targetName='server.exe',
                            )]
)
