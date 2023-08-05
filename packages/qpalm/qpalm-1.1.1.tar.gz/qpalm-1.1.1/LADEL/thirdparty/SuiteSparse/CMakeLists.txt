cmake_minimum_required(VERSION 3.17)
project(LADEL_suitesparse)

# Find the 64-bit signed integer type in C (usually long on Linux, long long on
# Windows). Unfortunately, we cannot use the C99 int64_t, because the code adds
# an “unsigned” prefix to this type, and “unsigned int64_t” is invalid syntax.
include(IntegerType64.cmake)
if (NOT INTEGER_TYPE_64)
    find_64bit_int_type(INTEGER_TYPE_64)
    set(INTEGER_TYPE_64 ${INTEGER_TYPE_64} CACHE STRING "64-bit integer C type")
endif()

# SuiteSparse config
add_library(suitesparse_config-headers INTERFACE)
target_compile_definitions(suitesparse_config-headers INTERFACE
    SuiteSparse_long=${INTEGER_TYPE_64}
    SuiteSparse_long_max=INT64_MAX
    SuiteSparse_long_idd=PRId64
)
target_include_directories(suitesparse_config-headers INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/SuiteSparse_config>)
if (MSVC)
    target_compile_definitions(suitesparse_config-headers INTERFACE
        "SuiteSparse_long_id=\"%%\" PRId64")
else()
    target_compile_definitions(suitesparse_config-headers INTERFACE
        "SuiteSparse_long_id=\"%\" PRId64")
endif()

add_library(suitesparse_config-obj OBJECT
    "SuiteSparse_config/SuiteSparse_config.c")
target_link_libraries(suitesparse_config-obj PUBLIC suitesparse_config-headers)
set_target_properties(suitesparse_config-obj PROPERTIES C_VISIBILITY_PRESET hidden)

# SuiteSparse approximate minimal degree
add_library(amd-headers INTERFACE)
target_include_directories(amd-headers INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/AMD/Include>)
target_link_libraries(amd-headers INTERFACE suitesparse_config-headers)

set(AMD_SOURCES
    "AMD/Source/amd_1.c"
    "AMD/Source/amd_2.c"
    "AMD/Source/amd_aat.c"
    "AMD/Source/amd_control.c"
    "AMD/Source/amd_defaults.c"
    "AMD/Source/amd_dump.c"
    "AMD/Source/amd_global.c"
    "AMD/Source/amd_info.c"
    "AMD/Source/amd_order.c"
    "AMD/Source/amd_post_tree.c"
    "AMD/Source/amd_postorder.c"
    "AMD/Source/amd_preprocess.c"
    "AMD/Source/amd_valid.c"
)
# Compile as integer version
add_library(amd_c_int-obj OBJECT ${AMD_SOURCES})
target_link_libraries(amd_c_int-obj PUBLIC amd-headers)
target_link_libraries(amd_c_int-obj PUBLIC suitesparse_config-obj)
target_compile_definitions(amd_c_int-obj PRIVATE DINT)
set_target_properties(amd_c_int-obj PROPERTIES C_VISIBILITY_PRESET hidden)

# Compile as long (or long long) version
add_library(amd_c_long-obj OBJECT ${AMD_SOURCES})
target_link_libraries(amd_c_long-obj PUBLIC amd-headers)
target_link_libraries(amd_c_long-obj PUBLIC suitesparse_config-obj)
target_compile_definitions(amd_c_long-obj PRIVATE DLONG)
set_target_properties(amd_c_long-obj PROPERTIES C_VISIBILITY_PRESET hidden)

# Link both versions
add_library(ladel_amd STATIC $<TARGET_OBJECTS:amd_c_int-obj>
                             $<TARGET_OBJECTS:amd_c_long-obj>
                             $<TARGET_OBJECTS:suitesparse_config-obj>)
target_link_libraries(ladel_amd INTERFACE amd-headers)
