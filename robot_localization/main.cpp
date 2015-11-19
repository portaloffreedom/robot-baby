#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

#include "process.h"
#include "qr.h"

/**
 * Setups the camera and returns false if something goes wrong.
 */
bool setupCamera(cv::VideoCapture &capture) {
    if (!capture.isOpened()) //if this fails, try to open as a video camera, through the use of an integer param
        capture.open(0);
    if (!capture.isOpened()) {
        std::cerr << "Failed to open the video device, video file or image sequence!\n" << std::endl;
        return false;
    }
    
    capture.set(CV_CAP_PROP_FRAME_WIDTH,1600);
    capture.set(CV_CAP_PROP_FRAME_HEIGHT,1200);
    
    cv::Mat image;
    capture >> image;
    if(image.empty()) {
        std::cerr << "ERR: Unable to query image from capture device.\n" << std::endl;
        return false;
    }
    return true;
}

////////////////////////////////////////////////////
// This program demonstrates the usage of SURF_OCL.
// use cpu findHomography interface to calculate the transformation matrix
int main(int argc, char* argv[])
{
    const char* keys =
        "{ h | help     | false           | print help message  }"
        "{ l | left     |                 | specify left image  }"
        "{ r | right    |                 | specify right image }"
        "{ o | output   | SURF_output.jpg | specify output save path (only works in CPU or GPU only mode) }"
        "{ c | use_cpu  | false           | use CPU algorithms  }"
        "{ a | use_all  | false           | use both CPU and GPU algorithms}";

    cv::CommandLineParser cmd(argc, argv, keys);
    if (cmd.get<bool>("help"))
    {
        std::cout << "Usage: surf_matcher [options]" << std::endl;
        std::cout << "Available options:" << std::endl;
        cmd.printParams();
        return EXIT_SUCCESS;
    }

    cv::Mat cpu_img1, cpu_img2;
    bool useCPU = cmd.get<bool>("c");
    bool useGPU = false;
    bool useALL = cmd.get<bool>("a");

    cv::string outpath = cmd.get<std::string>("o");

    cpu_img1 = cv::imread(cmd.get<std::string>("l"));
    CV_Assert(!cpu_img1.empty());

    cpu_img2 = cv::imread(cmd.get<std::string>("r"));
    CV_Assert(!cpu_img2.empty());

#ifdef USE_GPU
    
    if (useALL)
        useCPU = useGPU = false;
    else if(!useCPU && !useALL)
        useGPU = true;
    
#endif
    
    //staticFindLeftInRight(cpu_img1, cpu_img2, useALL, useCPU, useGPU, outpath);
    
    cv::VideoCapture capture( CV_CAP_ANY ); //try to open string, this will attempt to open it as a video file or image sequence
    if (!setupCamera(capture)) {
        return 1;
    }
    
    findQr(capture);
    
//     return process(capture, cpu_img1, useGPU);
    return EXIT_SUCCESS;
}
