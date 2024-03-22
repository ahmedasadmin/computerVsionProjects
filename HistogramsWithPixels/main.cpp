#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <vector>


class Histogram1D{

    private:

    int histSize[1];
    float hranges[2];
    const float* ranges[1];
    int channels[1];


    public:

    Histogram1D(){

        // prepare default arguments for 1D histogram 
        histSize[0] = 256;
        hranges[0] = 0.0;
        hranges[1] = 256.0;
        ranges[0] = hranges;
        channels[0] = 0;
    }      /// constructor

    // Computes the 1D histogram.

    cv::Mat getHistogram(const cv::Mat& image){
        
        cv::Mat hist;

        // Compute histogram 
        cv::calcHist(&image,
        1,
        channels,
        cv::Mat(),
        hist,
        1,
        histSize,
        ranges
        );

        return hist;
    } 
    // 
    cv::Mat getImageOfHistogram(const cv::Mat& hist, 
                                             int zoom);
    // Compute  the 1D histogram and returns an image of it.

    cv::Mat  getHistogramImage(const cv::Mat& image, 
                                int zoom=1){
        
        // Compute histogram  first.

        cv::Mat hist = getHistogram(image);

        // Create image of Histogram

        return getImageOfHistogram(hist, zoom);
                                    
    }

    
};
// Create an image representating a histogram 
    cv::Mat Histogram1D::getImageOfHistogram(const cv::Mat& hist, 
                                             int zoom){

        // Get min and max bin values

        double maxValue = 0;
        double minValue = 0;

        cv::minMaxLoc(hist, &minValue, &maxValue, 0, 0);

        // get hist size

        int histSize = hist.rows;

        // Square image on which to display histogram
        
        cv::Mat histImg(histSize*zoom,
                        histSize*zoom, CV_8U, cv::Scalar(255));

        // set highest point at 90% of nbins (i.e image height)

        int hpt = static_cast<int>(0.9*histSize);

        // Draw vertical line for each bin 
        
        for (int h=0; h<histSize; h++){
            float binVal = hist.at<float>(h);
        
            if(binVal>0){
                int intensity = static_cast<int>(binVal*hpt/maxValue);
                cv::line(histImg, cv::Point(h*zoom, histSize*zoom),
                        cv::Point(h*zoom, (histSize - intensity)*zoom),
                            cv::Scalar(0), zoom);
            }
        }

        return histImg;
    }

int main(){

    cv::Mat image = cv::imread("ax.png",
                                0);

    Histogram1D h;

    // Compute the histogram 
    cv::Mat histo = h.getHistogram(image);

    // Loop  over  each bin 
    for (int i=0; i<256; i++){

        std::cout << i << " = "
                  << histo.at<float>(i) << std::endl;
   
    }

    // Thresholding the image 

    cv::Mat threshold;
    cv::threshold(image,
                  threshold,
                  50,
                  255,
                  cv::THRESH_BINARY);



    // Display a histogram as an image 

    cv::namedWindow("Histogram");
    cv::imshow("Histogram", h.getHistogramImage(image));
    cv::imshow("ThresholdImage", threshold);
    
    
    // hold 

    cv::waitKey();

    return 0;
}