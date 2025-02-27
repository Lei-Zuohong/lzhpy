from distutils.core import setup, Extension
from Cython.Build import cythonize
from Cython.Compiler import Options


extensions = []
extensions.append(Extension(name='lzhsta.cregress.preload.core',
                            sources=['src/lzhsta/cregress/preload/core.pyx'],
                            define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')],
                            extra_compile_args=['-fopenmp', '-w'],
                            extra_link_args=['-fopenmp'],
                            language='c++'))
extensions.append(Extension(name='lzhsta.cregress.selfrsd.core',
                            sources=['src/lzhsta/cregress/selfrsd/core.pyx'],
                            define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')],
                            extra_compile_args=['-fopenmp', '-w'],
                            extra_link_args=['-fopenmp'],
                            language='c++'))
extensions.append(Extension(name='lzhsta.cregress.storersd.core',
                            sources=['src/lzhsta/cregress/storersd/core.pyx'],
                            define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')],
                            extra_compile_args=['-fopenmp', '-w'],
                            extra_link_args=['-fopenmp'],
                            language='c++'))
setup(ext_modules=cythonize(extensions,
                            compiler_directives={'language_level': 3}))
