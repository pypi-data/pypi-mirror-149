include(GNUInstallDirs)

set(INSTALL_CMAKE_DIR "${CMAKE_INSTALL_LIBDIR}/cmake/ladel")

# Add the ladel library to the "export-set", install the library files
install(TARGETS ladel EXPORT ladelTargets
    RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
        COMPONENT shlib
    LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
        COMPONENT shlib
    ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}" 
        COMPONENT lib)
if (LADEL_USE_AMD)
    install(TARGETS ladel_amd amd-headers suitesparse_config-headers 
        EXPORT ladelTargets
        RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
            COMPONENT shlib
        LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
            COMPONENT shlib
        ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}" 
            COMPONENT lib)
endif()

# Install the header files
install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/include/"
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
        COMPONENT dev
        FILES_MATCHING REGEX "/.*\.[hti](pp)?$")

# Install the export set for use with the install-tree
install(EXPORT ladelTargets 
    FILE ladelTargets.cmake
    DESTINATION "${INSTALL_CMAKE_DIR}" 
        COMPONENT dev
    NAMESPACE ${PROJECT_NAME}::)

# Generate the config file that includes the exports
include(CMakePackageConfigHelpers)
configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/Config.cmake.in"
    "${PROJECT_BINARY_DIR}/ladelConfig.cmake"
    INSTALL_DESTINATION "${INSTALL_CMAKE_DIR}"
    NO_SET_AND_CHECK_MACRO
    NO_CHECK_REQUIRED_COMPONENTS_MACRO)
write_basic_package_version_file(
    "${PROJECT_BINARY_DIR}/ladelConfigVersion.cmake"
    VERSION "${PROJECT_VERSION}"
    COMPATIBILITY SameMajorVersion)

# Install the ladelConfig.cmake and ladelConfigVersion.cmake
install(FILES
    "${PROJECT_BINARY_DIR}/ladelConfig.cmake"
    "${PROJECT_BINARY_DIR}/ladelConfigVersion.cmake"
    DESTINATION "${INSTALL_CMAKE_DIR}" 
        COMPONENT dev)

# Add all targets to the build tree export set
export(EXPORT ladelTargets
    FILE "${PROJECT_BINARY_DIR}/ladelTargets.cmake"
    NAMESPACE ${PROJECT_NAME}::)
