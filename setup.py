from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='etf data loader',
    ext_modules=cythonize('etf_data_loader.pyx'),
)