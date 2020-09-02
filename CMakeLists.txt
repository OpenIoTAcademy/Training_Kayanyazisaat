# Select system name Generic and change it to proper by target architecture settings files
set(CMAKE_SYSTEM_NAME Generic)
cmake_minimum_required(VERSION 3.12)

if(NOT DEFINED ARCH)
    set(ARCH native)
endif()

string(TOLOWER ${ARCH} ARCH)

if(ARCH STREQUAL "native")
    message(STATUS "Emulator system selected for compile")
    set(NAME_OF_PROJECT KayanyaziEmulator)
    set(DESCRIPTION_OF_RPOJECT "Kayan Yazi emulator compilation")
elseif(ARCH STREQUAL "arm")
    message(STATUS "ARM none-eabi architecture selected")
elseif(ARCH STREQUAL "armhf")
    message(STATUS "ARM linux-gnueabihf architecture selected")
else()
    message(FATAL_ERROR "Unknown architecture selected. Will stop now.")
endif()

if(NOT EXISTS ${CMAKE_SOURCE_DIR}/environment/${ARCH}/system.cmake)
    message(FATAL_ERROR "Target system settings file is missing. Please provide proper settings file.")
endif()

project(${NAME_OF_PROJECT}      # Project name
        VERSION 0.0.1           # Project Version
        DESCRIPTION ${DESCRIPTION_OF_RPOJECT}
        LANGUAGES C CXX ASM
        )

set(MODULES_SOURCE_DIR ${${CMAKE_PROJECT_NAME}_SOURCE_DIR}/source)
set(DRIVERS_SOURCE_DIR ${${CMAKE_PROJECT_NAME}_SOURCE_DIR}/Drivers)

# Create Main Project executable
add_executable(${CMAKE_PROJECT_NAME})

include("${CMAKE_SOURCE_DIR}/environment/${ARCH}/system.cmake")
if(ARCH STREQUAL "native")
    # Add main.c proejct. 
    target_include_directories(${CMAKE_PROJECT_NAME} PUBLIC ${${CMAKE_PROJECT_NAME}_SOURCE_DIR}/projects/gcc_host/inc)
    target_sources(${CMAKE_PROJECT_NAME} PUBLIC ${${CMAKE_PROJECT_NAME}_SOURCE_DIR}/projects/gcc_host/main.c)
    target_sources(${CMAKE_PROJECT_NAME} PUBLIC ${${CMAKE_PROJECT_NAME}_SOURCE_DIR}/projects/gcc_host/ky_socket.c)
endif()

# Add submodules to the project. Each submodule should have it's own CMakeLists.txt 
add_subdirectory(${DRIVERS_SOURCE_DIR}/gpio)
target_compile_options(${CMAKE_PROJECT_NAME} PUBLIC "-O0" "-g3" "-DDEBUG")

# Set C/C++ compiler settings
set(CMAKE_ASM_COMPILER  "${COMPILER_PREFIX}gcc -x assembler-with-cpp")
set(CMAKE_C_COMPILER    ${COMPILER_PREFIX}gcc)
set(CMAKE_CXX_COMPILER  ${COMPILER_PREFIX}g++)
set(CMAKE_OBJCOPY       ${COMPILER_PREFIX}objcopy)
set(CMAKE_OBJDUMP       ${COMPILER_PREFIX}objdump)
message(STATUS "Compiler prefix =" ${COMPILER_PREFIX})

# Include Splint static analysis tool
#include(${CMAKE_SOURCE_DIR}/environment/cmakeTools/splint.cmake)

