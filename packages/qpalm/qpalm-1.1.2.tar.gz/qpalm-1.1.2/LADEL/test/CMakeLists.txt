include(GoogleTest)
find_package(GTest REQUIRED CONFIG)

add_executable(ladel_run_all_tests
    "src/test_scale.cpp"
    "src/test_matvec.cpp"
    "src/test_matmat.cpp"
    "src/test_upper_diag.cpp"
    "src/test_etree.cpp"
    "src/test_postorder.cpp"
    "src/test_transpose.cpp"
    "src/test_col_counts.cpp"
    "src/test_permutation.cpp"
    "src/test_ldl.cpp"
    "src/test_rank1_mod.cpp"
    "src/test_row_mod.cpp"
    "src/test_add.cpp"
    "src/test_submatrix.cpp"
    "src/test_print.cpp"
)

target_include_directories(ladel_run_all_tests
    PRIVATE include
            include/Minunit
)

target_link_libraries(ladel_run_all_tests PRIVATE ladel)
target_link_libraries(ladel_run_all_tests PRIVATE GTest::gtest_main)

gtest_discover_tests(ladel_run_all_tests DISCOVERY_TIMEOUT 60)
