#ifndef __PROCESS_H__
#define __PROCESS_H__
#include "opencv2/core/core.hpp"

int process(cv::VideoCapture& capture, const cv::Mat& target, bool useGPU);

void staticFindLeftInRight(cv::Mat &left, cv::Mat &right, bool useALL, bool useCPU, bool useGPU, cv::string outpath);

#endif 
