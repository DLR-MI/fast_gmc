cmake_minimum_required(VERSION 3.0)
project(nms_variance CXX)

set(CMAKE_CXX_STANDARD 14)

# Find OpenCV (required for this)
find_package(OpenCV REQUIRED)

message(${OpenCV_INCLUDE_DIRS})
message(${OpenCV_LIBS})

add_subdirectory(extern/pybind11)
pybind11_add_module(gmc_pybind gmc_py.cpp)
target_include_directories(gmc_pybind PRIVATE ${OpenCV_INCLUDE_DIRS})
target_link_libraries(gmc_pybind PUBLIC ${OpenCV_LIBS})

