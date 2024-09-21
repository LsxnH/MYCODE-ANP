#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "WorkDir::PhysicsAnpWH" for configuration "RelWithDebInfo"
set_property(TARGET WorkDir::PhysicsAnpWH APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(WorkDir::PhysicsAnpWH PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libPhysicsAnpWH.so"
  IMPORTED_SONAME_RELWITHDEBINFO "libPhysicsAnpWH.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS WorkDir::PhysicsAnpWH )
list(APPEND _IMPORT_CHECK_FILES_FOR_WorkDir::PhysicsAnpWH "${_IMPORT_PREFIX}/lib/libPhysicsAnpWH.so" )

# Import target "WorkDir::PhysicsAnpBase" for configuration "RelWithDebInfo"
set_property(TARGET WorkDir::PhysicsAnpBase APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(WorkDir::PhysicsAnpBase PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libPhysicsAnpBase.so"
  IMPORTED_SONAME_RELWITHDEBINFO "libPhysicsAnpBase.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS WorkDir::PhysicsAnpBase )
list(APPEND _IMPORT_CHECK_FILES_FOR_WorkDir::PhysicsAnpBase "${_IMPORT_PREFIX}/lib/libPhysicsAnpBase.so" )

# Import target "WorkDir::PhysicsAnpData" for configuration "RelWithDebInfo"
set_property(TARGET WorkDir::PhysicsAnpData APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(WorkDir::PhysicsAnpData PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libPhysicsAnpData.so"
  IMPORTED_SONAME_RELWITHDEBINFO "libPhysicsAnpData.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS WorkDir::PhysicsAnpData )
list(APPEND _IMPORT_CHECK_FILES_FOR_WorkDir::PhysicsAnpData "${_IMPORT_PREFIX}/lib/libPhysicsAnpData.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
