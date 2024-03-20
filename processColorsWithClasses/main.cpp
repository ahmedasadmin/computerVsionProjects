#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <vector>

class ColorDetector {
    private:

    // minimum acceptance distance
    int maxDist;

    // target color 
    cv::Vec3b target;

    // image containing resulting binary map

    cv::Mat result;

    public:

    // empty constructor 
    // default parameter initialization here.

    ColorDetector() : maxDist(100), target(0, 0, 0){} // initializer list constructor 

    // Sets the color distance threshold
    // Threshold must be positive,
    // otherwise distance threshold is set to 0.

    // full constructor

    ColorDetector(uchar blue, uchar green, uchar red,
                  int maxDist=100): maxDist(maxDist){

                    // target color

                    setTargetColor(blue, green, red);
    }
    cv::Mat operator() (const cv::Mat& image){
    
        cv::Mat output;

        // compute absolute difference with target color 

        cv::absdiff(image, cv::Scalar(target), output);

        // split the channels into 3 images

        std::vector<cv::Mat> images;
        cv::split(output, images);

        // add the 3 channels 

        output = images[0] + images[1] + images[2];

        // apply threshold 

        cv::threshold(output,                  /// input image
                    output,                  /// output image
                    maxDist,                 /// threshold
                    255,                     /// max value
                    cv::THRESH_BINARY_INV);  /// thresholding mode
        return output;

    }
    void setColorDistanceThreshold(int distance){
        
        if (distance < 0)
            distance=0;
        maxDist = distance;

    }

    // Gets the color distance threshold 
    
    int getColorDistanceThreshold() const {

        return maxDist;
    }

    // Sets the color to be detected 
    
    void setTargetColor(uchar blue,
                        uchar green,
                        uchar red){
        // BGR order 

         target = cv::Vec3b(blue, green, red);

    }
    void setTargetColor(cv::Vec3b color){
        target = color;
    }

    //  Gets the color to be detected 

    cv::Vec3b getTargetColor() const{
        
        return target;
    }
    cv::Mat process(const cv::Mat& image);


};
cv::Mat ColorDetector::process(const cv::Mat& image){
    cv::Mat output;

    // compute absolute difference with target color 

    cv::absdiff(image, cv::Scalar(target), output);

    // split the channels into 3 images

    std::vector<cv::Mat> images;
    cv::split(output, images);

    // add the 3 channels 

    output = images[0] + images[1] + images[2];

    // apply threshold 

    cv::threshold(output,                  /// input image
                  output,                  /// output image
                  maxDist,                 /// threshold
                  255,                     /// max value
                  cv::THRESH_BINARY_INV);  /// thresholding mode
    return output;
}

int main(){

    ColorDetector colordetector(160, 250, 250,       /// color
                                100);       /// thresholddd call
    cv::Mat image = cv::imread("1.jpg");
      cv::resize(image, image, cv::Size(499, 399));
    cv::Mat result = colordetector(image);
    
    cv::imshow("colorDetectoin", result);
    cv::imshow("coloredImage", image);
    
    cv::waitKey();                     /// press any key to exit.
    return 0;
}