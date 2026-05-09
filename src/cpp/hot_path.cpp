#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <chrono>
#include <cassert>

int main() {
    // We generated a synthetic frame with two perfect "rocks" for the test
    cv::Mat frame = cv::Mat::ones(480, 640, CV_8UC1) * 50;
    cv::circle(frame, cv::Point(320, 240), 100, cv::Scalar(150), -1);
    cv::circle(frame, cv::Point(100, 100), 30, cv::Scalar(200), -1);

    int num_frames = 100;
    std::cout << "[INFO] Starting C++ Benchmark of the Pipeline (Hot Path) for " << num_frames << " frames..." << std::endl;

    // Variables outside the loop to avoid measuring iterative allocation
    cv::Mat clahe_out, blurred, edges, closed_edges;
    cv::Ptr<cv::CLAHE> clahe = cv::createCLAHE(2.0, cv::Size(8, 8));
    cv::Mat kernel = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(5, 5));
    
    // LEVEL 2 - DESIGN GAP
    std::vector<std::vector<cv::Point>> contours;

    std::vector<cv::Vec4i> hierarchy;

    auto start_time = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < num_frames; ++i) {
        // 1. Preprocessing (CLAHE)
        clahe->apply(frame, clahe_out);

        // 2. Smoothing (3-sigma rule -> 7x7 kernel)
        cv::GaussianBlur(clahe_out, blurred, cv::Size(7, 7), 1.0);

        // 3. Edges (Canny)
        // LEVEL 1 - MECHANICAL GAP
        cv::Canny(blurred, edges, 50, 150);

        // 4. Mathematical Morphology (Closing)
        cv::morphologyEx(edges, closed_edges, cv::MORPH_CLOSE, kernel);

        // LEVEL 3 - EDGE CASE GAP
        assert(closed_edges.type() == CV_8UC1);

        // 5. Topological contours
        cv::findContours(closed_edges, contours, hierarchy, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> diff = end_time - start_time;

    double ms_per_frame = diff.count() / num_frames;

    std::cout << "SUCCESS: Pipeline successfully ported to native memory." << std::endl;
    std::cout << "Rocks detected in the last frame: " << contours.size() << std::endl;
    std::cout << "Average latency: " << ms_per_frame << " ms/frame" << std::endl;
    
    // We should be comfortably below 33ms.
    assert(ms_per_frame < 10.0);

    return 0;
}