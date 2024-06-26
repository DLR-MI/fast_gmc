#include <iostream>
#include <typeinfo>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <string>

#include "opencv2/core.hpp"
#include "opencv2/video.hpp"
#include "opencv2/videostab.hpp"

namespace py = pybind11;

/**
 * Wrapper function that perform global camera compensation using OpenCVs videostab class.
 * Adapted and modified from: https://github.com/hustvl/SparseTrack/blob/main/python_module.cpp
 * @param currFrame Current video frame
 * @param prevFrame Previous video frame
 * @param downscale Downscaling factor to scale the frames and matrix.
 * @param model Can be "affine" or "homography" to indicate if affine or perspective warping should be performed.
 * @return 3x3 transformation matrix as Numpy Array.
**/
py::array_t<float> gmc(cv::Mat currFrame, cv::Mat prevFrame, int downscale, const std::string &model) {
    cv::videostab::MotionModel motionModel = model == "affine" ? cv::videostab::MM_SIMILARITY : (model == "homography" ? cv::videostab::MM_HOMOGRAPHY : cv::videostab::MM_UNKNOWN);
    if (motionModel == cv::videostab::MM_UNKNOWN)
	throw std::invalid_argument("Parameter 'model' must be 'affine' or 'homography'");

    cv::Mat frame, preframe;
    auto est = cv::makePtr<cv::videostab::MotionEstimatorRansacL2>(motionModel);
    auto kbest = cv::makePtr<cv::videostab::KeypointBasedMotionEstimator>(est);
    cv::Size downSize(currFrame.cols / downscale, currFrame.rows / downscale);
    cv::resize(currFrame, frame, downSize, cv::INTER_LINEAR);//

    cv::Mat warp = cv::Mat::eye(3, 3, CV_32F);

    if (!prevFrame.empty()) {
        cv::resize(prevFrame, preframe, downSize, cv::INTER_LINEAR);
        bool ok;
        warp = kbest->estimate(preframe, frame, &ok);

        if (!ok) {
            std::cout << "WARNING: Warp not ok" << std::endl;
        }

        warp.convertTo(warp, CV_32F);
        warp.at<float>(0, 2) *= downscale;
        warp.at<float>(1, 2) *= downscale;
    }

    return {
            {3, 3},
            {3 * sizeof(float), sizeof(float)},
            reinterpret_cast<float *>(warp.data)};
}

PYBIND11_MODULE(gmc_pybind, m) {
    m.def("GMC", [](py::array_t<uint8_t> &curr_frame, py::array_t<uint8_t> &prev_frame, int downscale, const std::string &model) {
        cv::Mat currFrame(curr_frame.shape(0), curr_frame.shape(1), CV_8UC3, (unsigned char *) curr_frame.data());
        cv::Mat prevFrame(prev_frame.shape(0), prev_frame.shape(1), CV_8UC3, (unsigned char *) prev_frame.data());
        return gmc(currFrame, prevFrame, downscale, model);
    }, "Global camera motion compensation using OpenCVs video stabilization classes.");
}
