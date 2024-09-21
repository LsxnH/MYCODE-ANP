#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "WorkDir::PhysicsAnpProdLib" for configuration "RelWithDebInfo"
set_property(TARGET WorkDir::PhysicsAnpProdLib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(WorkDir::PhysicsAnpProdLib PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libPhysicsAnpProdLib.so"
  IMPORTED_SONAME_RELWITHDEBINFO "libPhysicsAnpProdLib.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS WorkDir::PhysicsAnpProdLib )
list(APPEND _IMPORT_CHECK_FILES_FOR_WorkDir::PhysicsAnpProdLib "${_IMPORT_PREFIX}/lib/libPhysicsAnpProdLib.so" )

# Import target "WorkDir::PhysicsAnpProd" for configuration "RelWithDebInfo"
set_property(TARGET WorkDir::PhysicsAnpProd APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(WorkDir::PhysicsAnpProd PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libPhysicsAnpProd.so"
  IMPORTED_NO_SONAME_RELWITHDEBINFO "TRUE"
  )

list(APPEND _IMPORT_CHECK_TARGETS WorkDir::PhysicsAnpProd )
list(APPEND _IMPORT_CHECK_FILES_FOR_WorkDir::PhysicsAnpProd "${_IMPORT_PREFIX}/lib/libPhysicsAnpProd.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
