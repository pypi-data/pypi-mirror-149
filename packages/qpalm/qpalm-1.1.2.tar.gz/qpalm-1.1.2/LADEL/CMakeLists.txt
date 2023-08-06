cmake_minimum_required(VERSION 3.17)
project(LADEL-dev)
enable_testing()

# Add coverage target
option(LADEL_WITH_COVERAGE
    "Generate coverage information." Off)
if (LADEL_WITH_COVERAGE)
    add_custom_target(coverage
        ${CMAKE_CURRENT_LIST_DIR}/scripts/coverage.sh
        ${CMAKE_CXX_COMPILER_ID}
        ${CMAKE_CXX_COMPILER_VERSION}
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR})
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --coverage -fno-inline")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage -fno-inline")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --coverage")
    add_dependencies(coverage ladel_run_all_tests)
endif()

# TODO: add warning flags

add_subdirectory(LADEL)
add_subdirectory(test)