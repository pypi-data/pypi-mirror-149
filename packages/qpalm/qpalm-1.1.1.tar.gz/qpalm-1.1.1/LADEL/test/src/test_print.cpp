#include <minunit.h>

#include <ladel_debug_print.h>
#include <ladel_global.h>

#include <cstdarg>
#include <cstdio>

constexpr size_t NROW  = 4;
constexpr size_t NCOL  = 5;
constexpr size_t NZMAX = 11;

static char buffer[1024] = {'\0'};
static size_t buffer_idx = 0;

static int print_wrap(const char *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    size_t remaining = sizeof(buffer) - buffer_idx;
    auto ret         = vsnprintf(&buffer[buffer_idx], remaining, fmt, args);
    buffer_idx += ret;
    va_end(args);
    return ret;
}

TEST(Print, redirectPrint) {
    // clang-format off
    ladel_sparse_matrix *M = ladel_sparse_alloc(NROW, NCOL, NZMAX, UNSYMMETRIC, TRUE, FALSE);
    M->p[0] = 0; M->p[1] = 2; M->p[2] = 4; M->p[3] = 7; M->p[4] = 9; M->p[5] = 11;
    M->i[0] = 0; M->i[1] = 2; M->i[2] = 1; M->i[3] = 3; M->i[4] = 0; M->i[5] = 1; M->i[6] = 2; M->i[7] = 2; M->i[8] = 3; M->i[9] = 0; M->i[10] = 3;
    M->x[0] = 0.25; M->x[1] = 4.5; M->x[2] = -2; M->x[3] = -3; M->x[4] = 3.25; M->x[5] = 0.25; M->x[6] = 1.5; M->x[7] = 1.125; M->x[8] = 1.75; M->x[9] = 0.5; M->x[10] = -0.5;
    // clang-format on

    buffer_idx = 0; // Reset the print buffer
    // Set our custom `print_wrap` function as the printing function for LADEL
    auto old   = ladel_set_print_config_printf(&print_wrap);
    // Cause LADEL to print something
    ladel_print_sparse_matrix_matlab(M);
    // Restore the previous print function
    auto res = ladel_set_print_config_printf(&printf);
    // Did we get our custom wrapper back?
    EXPECT_EQ(res, &print_wrap);
    // Did we go out of bounds on the buffer?
    ASSERT_LE(buffer_idx, sizeof(buffer));
    // Null-terminate to be sure (shouldn't be necessary)
    buffer[buffer_idx] = '\0';
    // Check that the buffer contains what we expected
    auto expected =
        "M = sparse(4, 5);M(1, 1) = 2.5000000000000000e-01;M(3, 1) = "
        "4.5000000000000000e+00;M(2, 2) = -2.0000000000000000e+00;M(4, 2) = "
        "-3.0000000000000000e+00;M(1, 3) = 3.2500000000000000e+00;M(2, 3) = "
        "2.5000000000000000e-01;M(3, 3) = 1.5000000000000000e+00;M(3, 4) = "
        "1.1250000000000000e+00;M(4, 4) = 1.7500000000000000e+00;M(1, 5) = "
        "5.0000000000000000e-01;M(4, 5) = -5.0000000000000000e-01;\n";
    EXPECT_STREQ(buffer, expected);
    ladel_sparse_free(M);
}
