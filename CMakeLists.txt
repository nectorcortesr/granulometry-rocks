cmake_minimum_required(VERSION 3.10)
project(GranulometryCPP)

# We will use the modern standard C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Search for OpenCV in the system (required to continue)
find_package(OpenCV REQUIRED)
message(STATUS "OpenCV library status:")
message(STATUS "    version: ${OpenCV_VERSION}")
message(STATUS "    libraries: ${OpenCV_LIBS}")
message(STATUS "    include path: ${OpenCV_INCLUDE_DIRS}")

# Indicate the OpenCV headers
include_directories(${OpenCV_INCLUDE_DIRS})

# Create the executable binary
add_executable(hello_vision src/cpp/hello_vision.cpp)

# LEVEL 1 - MECHANICAL GAP
target_link_libraries(hello_vision ${OpenCV_LIBS})

add_executable(hot_path src/cpp/hot_path.cpp)
target_link_libraries(hot_path ${OpenCV_LIBS})