from contextlib import contextmanager
import os
import os.path as p
import subprocess as sub

self_path = p.dirname(p.abspath(__file__))

import numpy as np
from scipy.io import FortranFile

@contextmanager
def fortran_file(*args, **kwargs):
    f = FortranFile(*args, **kwargs)
    try:
        yield f
    finally:
        f.close()

@contextmanager
def working_directory(path):
    old_path = os.getcwd()
    sub.check_call(["mkdir", "-p", path])
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_path)

def compile_mim(nx, ny, layers):
    mim_path = p.join(p.dirname(self_path), "MIM.f90")
    sub.check_call(
        "cat %s " % (mim_path,) +
        "| sed 's/^    integer, parameter :: nx =.*$/    integer, parameter :: nx = %d/'" % (nx,) +
        "| sed 's/^    integer, parameter :: ny =.*$/    integer, parameter :: ny = %d/'" % (ny,) +
        "| sed 's/^    integer, parameter :: layers =.*$/    integer, parameter :: layers = %d/'" % (layers,) +
        "> MIM.f90", shell=True)
    sub.check_call(["gfortran", "-Ofast", "MIM.f90", "-o", "MIM"])

def write_input_f_plane(nx, ny):
    with fortran_file('fu.bin', 'w') as f:
        f.write_record(np.ones((nx, ny+1), dtype=np.float64)*10e-4)
    with fortran_file('fv.bin', 'w') as f:
        f.write_record(np.ones((nx+1, ny), dtype=np.float64)*10e-4)
    with fortran_file('wetmask.bin', 'w') as f:
        wetmask = np.ones((nx, ny), dtype=np.float64)
        wetmask[ 0, :] = 0
        wetmask[-1, :] = 0
        wetmask[ :, 0] = 0
        wetmask[ :,-1] = 0
        f.write_record(wetmask)
    with fortran_file('initH.bin', 'w') as f:
        f.write_record(np.ones((nx, ny), dtype=np.float64)*10e-4)

def test_f_plane_red():
    nx = 10
    ny = 10
    with working_directory(p.join(self_path, "f_plane_red")):
        sub.check_call(["rm", "-rf", "input/"])
        sub.check_call(["rm", "-rf", "output/"])
        sub.check_call(["mkdir", "-p", "output/"])
        with working_directory("input"):
            write_input_f_plane(nx, ny)
        compile_mim(nx, ny, 1)
        sub.check_call(["MIM"])
        sub.check_call(["diff", "-ru", "good-output/", "output/"])