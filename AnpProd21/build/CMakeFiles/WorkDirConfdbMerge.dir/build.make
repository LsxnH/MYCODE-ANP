# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.11

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/Cmake/3.11.0/Linux-x86_64/bin/cmake

# The command to remove a file.
RM = /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/Cmake/3.11.0/Linux-x86_64/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /hepustc/home/hengli/testarea/AnpProd21/source

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /hepustc/home/hengli/testarea/AnpProd21/build

# Utility rule file for WorkDirConfdbMerge.

# Include the progress variables for this target.
include CMakeFiles/WorkDirConfdbMerge.dir/progress.make

CMakeFiles/WorkDirConfdbMerge: x86_64-slc6-gcc62-opt/lib/libPhysicsAnpProd.confdb
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/hepustc/home/hengli/testarea/AnpProd21/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Built WorkDirConfdbMerge"
	/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/Cmake/3.11.0/Linux-x86_64/bin/cmake -E make_directory /hepustc/home/hengli/testarea/AnpProd21/build/x86_64-slc6-gcc62-opt/lib
	/cvmfs/atlas.cern.ch/repo/sw/software/21.2/AthAnalysis/21.2.65/InstallArea/x86_64-slc6-gcc62-opt/cmake/modules/scripts/mergeFiles.sh /hepustc/home/hengli/testarea/AnpProd21/build/x86_64-slc6-gcc62-opt/lib/WorkDir.confdb /hepustc/home/hengli/testarea/AnpProd21/build/CMakeFiles/WorkDirConfdbMergeFiles.txt

WorkDirConfdbMerge: CMakeFiles/WorkDirConfdbMerge
WorkDirConfdbMerge: CMakeFiles/WorkDirConfdbMerge.dir/build.make

.PHONY : WorkDirConfdbMerge

# Rule to build all files generated by this target.
CMakeFiles/WorkDirConfdbMerge.dir/build: WorkDirConfdbMerge

.PHONY : CMakeFiles/WorkDirConfdbMerge.dir/build

CMakeFiles/WorkDirConfdbMerge.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/WorkDirConfdbMerge.dir/cmake_clean.cmake
.PHONY : CMakeFiles/WorkDirConfdbMerge.dir/clean

CMakeFiles/WorkDirConfdbMerge.dir/depend:
	cd /hepustc/home/hengli/testarea/AnpProd21/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /hepustc/home/hengli/testarea/AnpProd21/source /hepustc/home/hengli/testarea/AnpProd21/source /hepustc/home/hengli/testarea/AnpProd21/build /hepustc/home/hengli/testarea/AnpProd21/build /hepustc/home/hengli/testarea/AnpProd21/build/CMakeFiles/WorkDirConfdbMerge.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/WorkDirConfdbMerge.dir/depend

