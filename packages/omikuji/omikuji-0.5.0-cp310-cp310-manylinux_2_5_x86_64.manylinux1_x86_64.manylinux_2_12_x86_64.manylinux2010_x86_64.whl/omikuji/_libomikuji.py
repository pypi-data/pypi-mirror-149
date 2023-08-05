# auto-generated file
__all__ = ['lib', 'ffi']

import os
from omikuji._libomikuji__ffi import ffi

lib = ffi.dlopen(os.path.join(os.path.dirname(__file__), '_libomikuji__lib.so'), 4098)
del os
