# CMakeLists.txt - CMake configuration file for EPA SWMMM 5.2

cmake_minimum_required (VERSION 3.11.0)
#project(swmm5 VERSION 5.2 LANGUAGES C)
project(swmm5)
find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
find_package(PythonExtensions REQUIRED)

# Add OpenMP package
find_package(OpenMP)
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()

if (MSVC)
# Set Visual Studio options:
#   /GL for whole program optimization
#   -MT for static link of runtime library functions
  set(CMAKE_C_FLAGS_RELEASE "/GL")
  add_definitions(-MT)
endif()

if (APPLE)
# Use relative paths for MacOS 
  set(INSTALL_NAME_DIR @executable_path/../lib)
  set(CMAKE_MACOSX_RPATH 1)
endif()

if (UNIX)
# Use relative paths for Linux 
  set(CMAKE_INSTALL_RPATH $ORIGIN)
  set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
endif()

# Configure file groups
file(GLOB SWMM_LIB_ALL RELATIVE ${PROJECT_SOURCE_DIR} swmm5/*.c swmm5/*.h swmm5/swmm5/* )

# Exclude main.c from the library build
list(REMOVE_ITEM SWMM_LIB_ALL "swmm5/swmm5/main.c")

# Configure the module
if(MSVC AND "${CMAKE_VS_PLATFORM_NAME}" MATCHES "(Win32)")
  message(STATUS "Configuring with swmm5.def mapping")
  add_library(_swmm5 MODULE ${SWMM_LIB_ALL} ${PROJECT_SOURCE_DIR}/swmm5/swmm5/swmm5.def)
  set_source_files_properties(${PROJECT_SOURCE_DIR}/swmm5/swmm5/swmm5.def PROPERTIES_HEADER_FILE_ONLY TRUE)

else()
  list(REMOVE_ITEM SWMM_LIB_ALL "swmm5/swmm5.def")
  add_library(_swmm5 MODULE ${SWMM_LIB_ALL})
  find_library(MATH_LIBRARY m)
  if(MATH_LIBRARY)
    target_link_libraries(_swmm5 PUBLIC ${MATH_LIBRARY} )
  endif()
endif()

## Configure the command line executable
#add_executable(runswmm ${PROJECT_SOURCE_DIR}/swmm5/swmm5/main.c)
#target_link_libraries(runswmm swmm5 ${PYTHON_LIBRARIES})
python_extension_module(_swmm)
install(TARGETS _swmm5 LIBRARY DESTINATION swmm5 )
