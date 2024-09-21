# Install script for directory: /hepustc/home/hengli/testarea/AnpProd21/source/PhysicsAnpProd

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/InstallArea/x86_64-slc6-gcc62-opt")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "RelWithDebInfo")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "0")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/src/PhysicsAnpProd" TYPE DIRECTORY FILES "/hepustc/home/hengli/testarea/AnpProd21/source/PhysicsAnpProd/" USE_SOURCE_PERMISSIONS REGEX "/\\.svn$" EXCLUDE REGEX "/\\.git$" EXCLUDE REGEX "/[^/]*\\~$" EXCLUDE)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process( COMMAND ${CMAKE_COMMAND}
      -E make_directory
      $ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/include )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process( COMMAND ${CMAKE_COMMAND}
         -E create_symlink ../src/PhysicsAnpProd/PhysicsAnpProd
         $ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/include/PhysicsAnpProd )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDebugx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE FILE OPTIONAL FILES "/hepustc/home/hengli/testarea/AnpProd21/build/x86_64-slc6-gcc62-opt/lib/libPhysicsAnpProdLib.so.dbg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY OPTIONAL FILES "/hepustc/home/hengli/testarea/AnpProd21/build/x86_64-slc6-gcc62-opt/lib/libPhysicsAnpProdLib.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libPhysicsAnpProdLib.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libPhysicsAnpProdLib.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/cvmfs/sft.cern.ch/lcg/releases/binutils/2.28-a983d/x86_64-slc6/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libPhysicsAnpProdLib.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDebugx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE FILE OPTIONAL FILES "/hepustc/home/hengli/testarea/AnpProd21/build/x86_64-slc6-gcc62-opt/lib/libPhysicsAnpProd.so.dbg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE MODULE OPTIONAL FILES "/hepustc/home/hengli/testarea/AnpProd21/build/x86_64-slc6-gcc62-opt/lib/libPhysicsAnpProd.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libPhysicsAnpProd.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libPhysicsAnpProd.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/cvmfs/sft.cern.ch/lcg/releases/binutils/2.28-a983d/x86_64-slc6/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libPhysicsAnpProd.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/python/PhysicsAnpProd" TYPE FILE OPTIONAL FILES "/hepustc/home/hengli/testarea/AnpProd21/build/x86_64-slc6-gcc62-opt/python/PhysicsAnpProd/PhysicsAnpProdConf.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process( COMMAND ${CMAKE_COMMAND} -E touch
      $ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/python/PhysicsAnpProd/__init__.py )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/jobOptions/PhysicsAnpProd" TYPE FILE RENAME "PhysicsAnpProd_ReadxAODFull.py" FILES "/hepustc/home/hengli/testarea/AnpProd21/source/PhysicsAnpProd/share/PhysicsAnpProd_ReadxAODFull.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/jobOptions/PhysicsAnpProd" TYPE FILE RENAME "PhysicsAnpProd_ReadxAODHIGG3.py" FILES "/hepustc/home/hengli/testarea/AnpProd21/source/PhysicsAnpProd/share/PhysicsAnpProd_ReadxAODHIGG3.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/jobOptions/PhysicsAnpProd" TYPE FILE RENAME "PhysicsAnpProd_ReadxAODr21.py" FILES "/hepustc/home/hengli/testarea/AnpProd21/source/PhysicsAnpProd/share/PhysicsAnpProd_ReadxAODr21.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/python/PhysicsAnpProd" TYPE FILE RENAME "PhysicsAnpProdUtils.py" FILES "/hepustc/home/hengli/testarea/AnpProd21/source/PhysicsAnpProd/python/PhysicsAnpProdUtils.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/python/PhysicsAnpProd" TYPE FILE RENAME "PhysicsAnpProdxAODFull.py" FILES "/hepustc/home/hengli/testarea/AnpProd21/source/PhysicsAnpProd/python/PhysicsAnpProdxAODFull.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/python/PhysicsAnpProd" TYPE FILE RENAME "PhysicsAnpProdxAODHIGG3.py" FILES "/hepustc/home/hengli/testarea/AnpProd21/source/PhysicsAnpProd/python/PhysicsAnpProdxAODHIGG3.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/python/PhysicsAnpProd" TYPE FILE RENAME "PhysicsAnpProdxAODr21.py" FILES "/hepustc/home/hengli/testarea/AnpProd21/source/PhysicsAnpProd/python/PhysicsAnpProdxAODr21.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/python/PhysicsAnpProd" TYPE FILE FILES "/hepustc/home/hengli/testarea/AnpProd21/build/x86_64-slc6-gcc62-opt/python/PhysicsAnpProd/PhysicsAnpProdUtils.pyc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/python/PhysicsAnpProd" TYPE FILE FILES "/hepustc/home/hengli/testarea/AnpProd21/build/x86_64-slc6-gcc62-opt/python/PhysicsAnpProd/PhysicsAnpProdxAODFull.pyc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/python/PhysicsAnpProd" TYPE FILE FILES "/hepustc/home/hengli/testarea/AnpProd21/build/x86_64-slc6-gcc62-opt/python/PhysicsAnpProd/PhysicsAnpProdxAODHIGG3.pyc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/python/PhysicsAnpProd" TYPE FILE FILES "/hepustc/home/hengli/testarea/AnpProd21/build/x86_64-slc6-gcc62-opt/python/PhysicsAnpProd/PhysicsAnpProdxAODr21.pyc")
endif()

