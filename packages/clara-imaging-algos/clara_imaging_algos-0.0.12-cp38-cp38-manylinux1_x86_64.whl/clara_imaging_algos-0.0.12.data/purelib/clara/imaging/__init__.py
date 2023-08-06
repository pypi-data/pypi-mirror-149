import os
import subprocess

def check_dependencies():
    cuda_lib = '/usr/local/cuda/targets/x86_64-linux/lib/libcudart.so'

    if os.path.exists(cuda_lib) is False:
        raise RuntimeError("Cuda 11.0 required.")


def update_lib_path():
    lib_path = os.path.abspath(os.path.dirname(__file__))
    subprocess.check_call(['patchelf', '--set-rpath', lib_path, os.path.join(lib_path, './algos.so')])

check_dependencies()
update_lib_path()

from . import algos
assert (algos is not None)

