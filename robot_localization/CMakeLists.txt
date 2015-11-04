cmake_minimum_required(VERSION 2.6)
project(robot_localization)

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


add_executable(robot_localization main.cpp)

target_link_libraries(robot_localization ${OPENCV_LINKER_LIBS} ${OPENCV_OCL_SAMPLES_REQUIRED_DEPS})

install(TARGETS robot_localization RUNTIME DESTINATION bin)
