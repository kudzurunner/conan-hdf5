from conans import ConanFile, CMake, tools
import os
import shutil

class Hdf5Conan(ConanFile):
    name = "hdf5"
    version = "1.10.4"
    license = "https://support.hdfgroup.org/ftp/HDF5/releases/COPYING"
    author = "KudzuRunner"
    url = "https://github.com/kudzurunner/conan-hdf5"
    description = "HDF5 C and C++ libraries"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    requires = "zlib/1.2.11@conan/stable"

    build_name = "build"

    def source(self):
        git = tools.Git(folder=self.name)
        git.clone("https://bitbucket.hdfgroup.org/scm/hdffv/hdf5.git", "hdf5-{}".format(self.version.replace(".", "_")))

        tools.replace_in_file("{}/CMakeLists.txt".format(self.name), "project (HDF5 C)",
                              '''project (HDF5 C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def configure(self):
        self.options["zlib"].shared = self.options.shared

    def build(self):
        os.mkdir(self.build_name)
        shutil.move("conanbuildinfo.cmake", self.build_name)
        cmake = CMake(self)
        cmake.definitions["HDF5_BUILD_EXAMPLES"] = "OFF"
        cmake.definitions["HDF5_BUILD_TOOLS"] = "OFF"
        cmake.definitions["HDF5_BUILD_HL_LIB"] = "OFF"
        cmake.definitions["HDF5_BUILD_CPP_LIB"] = "ON"
        cmake.definitions["HDF5_ENABLE_Z_LIB_SUPPORT"] = "ON"
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = self.package_folder
        if self.settings.compiler == "Visual Studio":
            cmake.definitions["CMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP"] = True
        cmake.configure(source_folder=self.name, build_folder=self.build_name)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("COPYING", src=self.name, keep_path=False)

    def package_info(self):
        debug_suffix = ("_D" if self.settings.build_type=="Debug" else "")
        if self.options.shared:
            self.cpp_info.libs = ["hdf5" + debug_suffix]
        else:
            self.cpp_info.libs = ["libhdf5" + debug_suffix]
        if tools.os_info.is_windows and self.options.shared:
            self.cpp_info.defines = ["H5_BUILT_AS_DYNAMIC_LIB"]