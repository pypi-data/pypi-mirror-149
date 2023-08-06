#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "hyperloglog::murmurhash3" for configuration "Release"
set_property(TARGET hyperloglog::murmurhash3 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(hyperloglog::murmurhash3 PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libmurmurhash3.so"
  IMPORTED_SONAME_RELEASE "libmurmurhash3.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS hyperloglog::murmurhash3 )
list(APPEND _IMPORT_CHECK_FILES_FOR_hyperloglog::murmurhash3 "${_IMPORT_PREFIX}/lib64/libmurmurhash3.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
