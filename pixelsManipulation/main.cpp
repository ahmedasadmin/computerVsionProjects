
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>


void salt(cv::Mat& image, int n){
    // 'n'is the number of noise points
    // 'image' is just image to add noise

    int i, j;

    for (int k=0; k<n; k++){
        i = std::rand()%image.cols;
        j=  std::rand()%image.rows;

        if(image.type() == CV_8UC1){
            image.at<uchar>(j,i) =  255;
        }
        else if(image.type() == CV_8UC3){
            image.at<cv::Vec3b>(j,i) [0] =  255;
            image.at<cv::Vec3b>(j,i )[1] =  100;
            image.at<cv::Vec3b>(j,i) [2] =  200;
        }
    }
}
void colorReduce(cv::Mat& image, int div=64){
    unsigned int nc = image.channels() * image.cols;
    for(int j=0; j<image.rows; j++){

        // get the address of row j
        uchar* data = image.ptr<uchar>(j);

        for (unsigned int i=0; i<nc; i++){
            data[i] = data[i]/div*div + div/2;
        }
    }
}
void colorReduceIter(cv::Mat image, int div=64){
    cv::Mat_<cv::Vec3b>::iterator it = image.begin<cv::Vec3b>();
    cv::Mat_<cv::Vec3b>::iterator itend = image.end<cv::Vec3b>();
    

    for (; it!=itend; ++it){

        (*it)[0] = (*it)[0] / div*div + div/2;
        (*it)[1] = (*it)[1] / div*div + div/2;
        (*it)[2] = (*it)[2] / div*div + div/2;
    }
}
void sharpen(const cv::Mat& image, cv::Mat& result){
    result.create(image.size(), image.type());
    int channels = image.channels(); // get the number of channels

    // can not access First and Last rows
    // same for colls
    // so, we can write loop as follow

    for(int j=0; j<image.rows-1; j++){

        const uchar* previous =
            image.ptr<const uchar> (j-1);
        const uchar* current =
            image.ptr<const uchar>(j);
        const uchar* next = 
            image.ptr<const uchar>(j+1);
        
        uchar* output  = result.ptr<uchar>(j);

        for(int i=channels; i<(image.cols-1)*channels; i++){
            *output++= cv::saturate_cast<uchar>(
                5*current[i]-current[i-channels] - 
                current[i+channels]-
                previous[i]-next[i]
            );
        }
    }
}
void sharpen2D(const cv::Mat& image, cv::Mat& result){
    // kernel used in filter 
    cv::Mat kernel(3, 3, CV_32F, cv::Scalar(0));
    
    kernel.at<float>(1,1)=5.0;
    kernel.at<float>(0,1)=-1.0;
    kernel.at<float>(2,1)=-1.0;
    kernel.at<float>(1,0)=-1.0;
    kernel.at<float>(1,2)=-1.0;

    cv::filter2D(image, result, image.depth(), kernel);

}
void wave(const cv::Mat& image, cv::Mat& result){
    //creating two mapping vars;;
    cv::Mat scrX(image.rows, image.cols, CV_32F);
    cv::Mat scrY(image.rows, image.cols, CV_32F);

    // Looping over every pixel
    for(int i=0; i<image.rows; i++){
        for(int j=0; j<image.cols; j++){
            scrX.at<float>(i, j) = j;     // remain on same cols
            scrY.at<float>(i, j) = i + 1*sin(j/10);
        }
    }

    cv::remap(image, result, scrX, scrY, cv::INTER_LINEAR);
}
void hflip(const cv::Mat& image, cv::Mat& result){
    //creating two mapping vars;;
    cv::Mat scrX(image.rows, image.cols, CV_32F);
    cv::Mat scrY(image.rows, image.cols, CV_32F);

    // Looping over every pixel
    for(int i=0; i<image.rows; i++){
        for(int j=0; j<image.cols; j++){
            scrX.at<float>(i, j) = image.cols-j-1;     // remain on same cols
            scrY.at<float>(i, j) = i;
        }
    }

    cv::remap(image, result, scrX, scrY, cv::INTER_LINEAR);
}
int main()
{

    cv::Mat image; // create an empty image 
    image = cv::imread("1.jpg");
    cv::Mat image2 = cv::imread("rainyDay.png");
    cv::resize(image, image, cv::Size(499, 399));
    cv::resize(image2, image2, cv::Size(499, 399));
    
    if(image.empty()||image2.empty()){

        std::cerr << "Can't  load image" << std::endl;
        std::cerr << "please check path well";
        return 1;
    }

    // define image windows
    // convert to grayscale 
    cv::Mat outImage;
    // cv::cvtColor(image, image, cv::COLOR_BGR2GRAY);
    // cv::cvtColor(image2, image2, cv::COLOR_BGR2GRAY);
    
    int64 start = cv::getTickCount();
    //  colorReduceIter(image, 50);
    // sharpen2D(image, outImage);
    cv::add(image, image2, outImage);
    // wave(outImage, outImage);
    hflip(image, outImage);
    _Float64 duration = (cv::getTickCount()- start)/ cv::getTickFrequency();
    
    //salt(image, 1000);
    std::cout << "image type: " << image.type() << " duration: " << duration << std::endl;

    cv::imshow("It is rainy day, isn't?", outImage);
    cv::waitKey(0);
    
    

}
