#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ngstd" for configuration "Release"
set_property(TARGET ngstd APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngstd PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/python3.8/site-packages/netgen_mesher_avx2.libs/libngstd.so"
  IMPORTED_SONAME_RELEASE "libngstd.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS ngstd )
list(APPEND _IMPORT_CHECK_FILES_FOR_ngstd "${_IMPORT_PREFIX}/lib/python3.8/site-packages/netgen_mesher_avx2.libs/libngstd.so" )

# Import target "ngbla" for configuration "Release"
set_property(TARGET ngbla APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngbla PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/python3.8/site-packages/netgen_mesher_avx2.libs/libngbla.so"
  IMPORTED_SONAME_RELEASE "libngbla.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS ngbla )
list(APPEND _IMPORT_CHECK_FILES_FOR_ngbla "${_IMPORT_PREFIX}/lib/python3.8/site-packages/netgen_mesher_avx2.libs/libngbla.so" )

# Import target "ngla" for configuration "Release"
set_property(TARGET ngla APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngla PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/python3.8/site-packages/netgen_mesher_avx2.libs/libngla.so"
  IMPORTED_SONAME_RELEASE "libngla.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS ngla )
list(APPEND _IMPORT_CHECK_FILES_FOR_ngla "${_IMPORT_PREFIX}/lib/python3.8/site-packages/netgen_mesher_avx2.libs/libngla.so" )

# Import target "ngfem" for configuration "Release"
set_property(TARGET ngfem APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngfem PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/python3.8/site-packages/netgen_mesher_avx2.libs/libngfem.so"
  IMPORTED_SONAME_RELEASE "libngfem.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS ngfem )
list(APPEND _IMPORT_CHECK_FILES_FOR_ngfem "${_IMPORT_PREFIX}/lib/python3.8/site-packages/netgen_mesher_avx2.libs/libngfem.so" )

# Import target "ngcomp" for configuration "Release"
set_property(TARGET ngcomp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngcomp PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/python3.8/site-packages/netgen_mesher_avx2.libs/libngcomp.so"
  IMPORTED_SONAME_RELEASE "libngcomp.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS ngcomp )
list(APPEND _IMPORT_CHECK_FILES_FOR_ngcomp "${_IMPORT_PREFIX}/lib/python3.8/site-packages/netgen_mesher_avx2.libs/libngcomp.so" )

# Import target "solve" for configuration "Release"
set_property(TARGET solve APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(solve PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/python3.8/site-packages/netgen_mesher_avx2.libs/libsolve.so"
  IMPORTED_SONAME_RELEASE "libsolve.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS solve )
list(APPEND _IMPORT_CHECK_FILES_FOR_solve "${_IMPORT_PREFIX}/lib/python3.8/site-packages/netgen_mesher_avx2.libs/libsolve.so" )

# Import target "ngsolve" for configuration "Release"
set_property(TARGET ngsolve APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngsolve PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/python3.8/site-packages/netgen_mesher_avx2.libs/libngsolve.so"
  IMPORTED_SONAME_RELEASE "libngsolve.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS ngsolve )
list(APPEND _IMPORT_CHECK_FILES_FOR_ngsolve "${_IMPORT_PREFIX}/lib/python3.8/site-packages/netgen_mesher_avx2.libs/libngsolve.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
