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


    void detectHScolor(const cv::Mat& image,
    double minHue, double maxHue,
    double minSat, double maxSat,
    cv::Mat& mask){

        // convert into HSV space

        cv::Mat hsv;
        cv::cvtColor(image, hsv, cv::COLOR_BGR2HSV);

        // split the 3 channels into 3 images

        std::vector<cv::Mat> channels;
        cv::split(hsv, channels);

        // Hue masking 
        cv::Mat hueMask;

        cv::Mat mask1;
        cv::threshold(channels[0], mask1, maxHue, 255, cv::THRESH_BINARY_INV);
        cv::Mat mask2;
        cv::threshold(channels[0], mask2, minHue, 255, cv::THRESH_BINARY);
        if (minHue < maxHue)
            hueMask = mask1 & mask2;
        else
            hueMask = mask1 | mask2;

        // Saturation masking  
        cv::Mat satMask;

        cv::threshold(channels[1], mask1, maxSat, 255, cv::THRESH_BINARY_INV);
        cv::threshold(channels[1], mask2, minSat, 255, cv::THRESH_BINARY);
       
        satMask = mask1 & mask2;


        // combine  mask

        mask = hueMask & satMask;
    }


};
cv::Mat ColorDetector::process(const cv::Mat& image){
    cv::Mat output;

    //e
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
    cv::Mat frame;
    cv::VideoCapture cap;
    // int deviceID = 0;
    int apiID = cv::CAP_ANY;

    cap.open("Board.mp4", apiID);
    if(!cap.isOpened()){

        std::cerr << "Oops, Unable to open camera" << std::endl;
        return -1;
    }
    std::cout << "Start program"<< std::endl
              << "Press any key to quit!." << std::endl;
    cv::Mat mask;

 
    while(true){
        
        cap.read(frame);
        if(frame.empty()){
            continue;
        }
        // ColorDetector colordetector(100, 100, 150,       /// color
        //                                 100);       /// thresholddd call
        //     // cv::Mat image = cv::imread("1.jpg");

        cv::Mat image = frame;
        ColorDetector skinDetector;
        skinDetector.detectHScolor(image,
        160, 10,
        25, 166,
        mask);
        // cv::resize(image, image, cv::Size(499, 399));
        // cv::Mat result = colordetector(image);
        

        // show masked image 
        
        cv::Mat detected(image.size(), CV_8UC3, cv::Scalar(0, 0, 0) );
        image.copyTo(detected, mask);

        cv::imshow("skin detector", detected);
        cv::imshow("Image", image);
        
        if(cv::waitKey(10) >= 0){
            break;
        }           /// press any key to exit.

    }


    return 0;   
}                   /// end main...!