cmake_minimum_required(VERSION 2.8)

project(pycoco)

set(CMAKE_CXX_STANDARD 98)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
include_directories(SYSTEM ${CONAN_INCLUDE_DIRS})
include_directories(${PROJECT_SOURCE_DIR}/pybind11/include)
include_directories(${PYTHON_INCLUDE_DIR})


add_library(pycoco SHARED pypoco.cpp)

install(TARGETS pycoco DESTINATION bin)

set_target_properties(pycoco PROPERTIES SUFFIX ".so")

# Strip unnecessary sections of the binary on Linux/Mac OS
if(APPLE)
    set_target_properties(pycoco PROPERTIES MACOSX_RPATH ".")
    set_target_properties(pycoco PROPERTIES LINK_FLAGS "-undefined dynamic_lookup ")
    if (NOT ${U_CMAKE_BUILD_TYPE} MATCHES DEBUG)
        add_custom_command(TARGET pycoco POST_BUILD COMMAND strip -u -r ${PROJECT_BINARY_DIR}/pycoco.so)
    endif()
else()
    if (NOT ${U_CMAKE_BUILD_TYPE} MATCHES DEBUG)
        add_custom_command(TARGET pycoco POST_BUILD COMMAND strip ${PROJECT_BINARY_DIR}/pycoco.so)
    endif()
endif()