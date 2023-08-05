import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": {"common", "project_logging", "client"}
}
setup(
    name="mess_client",
    version="0.8.7",
    description="mess_client",
    options={
        "build_exe": build_exe_options
    },
    executables=[Executable('client_script.py',
                            base='Win32GUI',
                            targetName='client.exe',
                            )]
)
