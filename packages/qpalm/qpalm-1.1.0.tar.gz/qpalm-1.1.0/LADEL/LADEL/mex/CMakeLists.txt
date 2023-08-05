cmake_minimum_required(VERSION 3.17)
project(LADEL-mex)

# Find the Matlab MEX compiler:
find_package(Matlab REQUIRED COMPONENTS MEX_COMPILER)
add_library(matlab_mex_headers INTERFACE)
target_include_directories(matlab_mex_headers SYSTEM 
    INTERFACE ${Matlab_INCLUDE_DIRS})

# Compile the utility library
add_library(mex_util OBJECT src/ladel_mex_util.c)
target_link_libraries(mex_util PUBLIC LADEL::ladel matlab_mex_headers)
target_include_directories(mex_util PUBLIC include)
add_library(LADEL::mex_util ALIAS mex_util)

# Create a target for compiling a MEX function:
matlab_add_mex(
    NAME ladel_mex                    # Name for use in Matlab
    SRC src/ladel_mex.c               # Source files to compile
    LINK_TO LADEL::mex_util           # Dependencies
)
if (NOT WIN32 AND NOT APPLE)
    # Matlab's C++ standard library is too old, so link it statically:
    target_link_options(ladel_mex PUBLIC -static-libstdc++ -static-libgcc)
endif()

# Install the final MEX file
install(FILES $<TARGET_FILE:ladel_mex>
        ladel.m
        EXCLUDE_FROM_ALL
        COMPONENT mex_interface
        DESTINATION @ladel)