cmake_minimum_required(VERSION 2.6)
project(robot_localization)

if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang" OR CMAKE_COMPILER_IS_GNUCXX)
    include(CheckCXXCompilerFlag)
    check_cxx_compiler_flag(--std=c++11 SUPPORTS_STD_CXX11)
    check_cxx_compiler_flag(--std=c++0x SUPPORTS_STD_CXX01)
    if(SUPPORTS_STD_CXX11)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --std=c++11")
        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --std=c++11")
    elseif(SUPPORTS_STD_CXX01)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --std=c++0x")
        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --std=c++0x")
    else()
        message(ERROR "Compiler does not support --std=c++11 or --std=c++0x.")
    endif()
endif()


set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -lpthread")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -lpthread")

include_directories("oscpack")

#TODO this is only for unix system. If you want to make it work on windows, add the right source files (win32 instead of posix folder)
set("OSCPACK_SRCS"
    oscpack/ip/posix/UdpSocket.cpp
    oscpack/osc/OscOutboundPacketStream.cpp
    oscpack/osc/OscReceivedElements.cpp
)

set("TUIO_SRCS" 
    TUIO/TuioClient.cpp
    TUIO/TuioContainer.cpp
    TUIO/TuioBlob.cpp
    TUIO/TuioDispatcher.cpp
    TUIO/TuioPoint.cpp
    TUIO/TuioTime.cpp
    TUIO/TuioObject.cpp
    TUIO/UdpReceiver.cpp
    TUIO/TuioCursor.cpp
    TUIO/OscReceiver.cpp
)

set("app_SRCS" main.cpp
    tuio.cpp
)


add_executable(robot_localization ${app_SRCS} ${TUIO_SRCS} ${OSCPACK_SRCS})

install(TARGETS robot_localization RUNTIME DESTINATION bin)
