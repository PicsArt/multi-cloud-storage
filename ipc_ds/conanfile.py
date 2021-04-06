from conans import ConanFile, tools, CMake
from distutils.sysconfig import get_python_inc
import distutils.sysconfig as sysconfig

# -DPYTHON_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
# -DPYTHON_LIBRARY=$(python -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))")

class PocoPyReuseConan(ConanFile):
    name = "PocoPy"
    version = "0.1"
    requires = "poco/1.9.4", "pybind11/2.3.0@conan/stable"
    settings = "os", "compiler", "arch", "build_type"
    exports = "*"
    generators = "cmake"
    build_policy = "missing"

    def build(self):
        cmake = CMake(self)
        pythonpaths = "-DPYTHON_INCLUDE_DIR={} -DPYTHON_LIBRARY={}".format(get_python_inc(), sysconfig.get_config_var('LIBDIR'))
        self.run('cmake .. %s %s' % ("-G 'Unix Makefiles'", pythonpaths))
        self.run("cmake .. --build . %s" % cmake.build_config)

    def package(self):
        self.copy('*.py*')
        self.copy("*.so")

    def package_info(self):
        self.env_info.PYTHONPATH.append(self.package_folder)
