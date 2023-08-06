import os
import numpy
from Cython.Build import cythonize

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    cpp_version = "c++11"
    define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
    if os.name == "nt":
        ext_comp_args = ['/openmp']
        ext_link_args = ['/openmp']

        library_dirs = [cg.mpir_path]
        libraries = []
    else:
        ext_comp_args = ['-fopenmp']
        ext_link_args = ['-fopenmp']

        library_dirs = []
        libraries = ["m"]

    config = Configuration('CDKM_pkg', parent_package, top_path)

    file_path = os.path.dirname(__file__)
    local_eigen = "Eigen339"
    eigen_path = os.path.join(file_path, local_eigen)

    cyname = "CDKM_"
    config.add_extension(cyname,
                         sources=[f'{cyname}.pyx'],
                         include_dirs = [numpy.get_include(), eigen_path],
                         language="c++",

                         extra_compile_args=ext_comp_args,
                         extra_link_args=ext_link_args,

                         library_dirs=library_dirs,
                         libraries=libraries,
                         depends=[f"{cyname}.pxd", f"{cyname}.pyx", "./Eigen339"]
                         #  define_macros=cg.define_macros,
                         )

    config.ext_modules = cythonize(config.ext_modules, compiler_directives={'language_level': 3})

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
