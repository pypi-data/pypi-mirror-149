# Thirdparty

LADEL includes the AMD module from SuiteSparse without any modifications.

One trivial modification has been made to `SuiteSparse_config.h`: the addition
of the line `#include <inttypes.h>`, to be able to access the `PRId64` constant.

Source: https://github.com/DrTimothyAldenDavis/SuiteSparse/tree/9d97e0a2fb3d03fac66cd45d3a84338b0a97f368
(downloaded on 25/01/2022)