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


find_package(OpenCV REQUIRED)

SET(OPENCV_OCL_SAMPLES_REQUIRED_DEPS opencv_core opencv_flann opencv_imgproc opencv_highgui
                                     opencv_ml opencv_video opencv_objdetect opencv_features2d
                                     opencv_calib3d opencv_legacy opencv_contrib opencv_ocl
                                     opencv_nonfree)

ocv_check_dependencies(${OPENCV_OCL_SAMPLES_REQUIRED_DEPS})
ocv_include_modules(${OPENCV_OCL_SAMPLES_REQUIRED_DEPS})

if(HAVE_OPENCL)
    ocv_include_directories(${OPENCL_INCLUDE_DIR})
endif()


add_executable(robot_localization main.cpp process.cpp qr.cpp)

target_link_libraries(robot_localization ${OPENCV_LINKER_LIBS} ${OPENCV_OCL_SAMPLES_REQUIRED_DEPS})

install(TARGETS robot_localization RUNTIME DESTINATION bin)
