#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    std::cout << "[INFO] Starting C++ vision engine..." << std::endl;

    // LEVEL 2 - DESIGN GAP
    cv::Mat img = cv::imread("test_rock.jpg", cv::IMREAD_GRAYSCALE);
    // LEVEL 3 - EDGE CASE GAP
    if (img.empty()) {
        // (Hint: Unlike Python where it may raise a TypeError later, in C++ imread fails silently returning an empty matrix if the image does not exist or is corrupted. Which boolean method of the cv::Mat class checks if the pointer has no data?)
        std::cerr << "[CRITICAL ERROR] The image test_rock.jpg could not be loaded or does not exist on disk." << std::endl;
        return -1;
    }

    std::cout << "[INFO] Image loaded successfully. Resolution: " 
              << img.cols << "x" << img.rows << std::endl;

    // Display the image
    cv::imshow("C++ Production", img);
    std::cout << "Press any key in the image window to exit..." << std::endl;
    cv::waitKey(0);

    return 0;
}