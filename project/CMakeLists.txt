cmake_minimum_required(VERSION 3.6)

set(OUTPUT_DIR ${CMAKE_SOURCE_DIR}/bin.Debug)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${OUTPUT_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${OUTPUT_DIR})
set(CMAKE_CXX_FLAGS "-O0 -g -std=c++11")
set(CMAKE_EXE_LINKER_FLAGS "-g")

project(project)

set(CMAKE_CXX_STANDARD 11)

add_executable(project main.cpp)