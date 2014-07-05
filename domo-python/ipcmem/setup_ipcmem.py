#! /usr/bin/env python
from distutils.core import setup, Extension

setup(name="ipcmem",
      version="1.0",
      ext_modules=[Extension("ipcmem", ["ipcmem.c"])])

