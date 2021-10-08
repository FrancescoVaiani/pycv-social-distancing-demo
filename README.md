# PyCV Social Distancing demo
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)

Small proof of concept of a software that evaluates distance of the subjects 
it captures from the camera and the relative distance between them.
The distance of the subjects is calculated using triangle similarity (further 
info in the [triangular similarity](#triangular-similarity) section)

## Execute project
### General Setup
Before starting, be sure to have `python 3`  and `pip` installed, then run
```bash
pip3 install -r requirements.txt
```

### Calibration phase
First you need to do the calibration phase 
```shell
python3 social_distancing.py calibrate --help
usage: social_distancing.py calibrate [-h] --distance DISTANCE [--videocameraindex VIDEOCAMERAINDEX]

optional arguments:
  -h, --help            show this help message and exit
  --distance DISTANCE, -d DISTANCE
                        Distance of the calibration face from camera
  --videocameraindex VIDEOCAMERAINDEX, -v VIDEOCAMERAINDEX
                        Video camera index
```
Get the distance between the subject's face and the camera (ie 30 cm) and run
```shell
python3 social_distancing.py calibrate -d 30
```
Don't move the subject until the percentage is 100% then take the number printed ad the end as
your calibration value
```shell
python3 social_distancing.py calibrate -d 30
100.0%
10385
```
### Run
Now you have all the data you need, we can now run the actual software.
```shell
python3 social_distancing.py run --help
usage: social_distancing.py run [-h] --calibrationresult CALIBRATIONRESULT [--threshold THRESHOLD] [--inches] [--videocameraindex VIDEOCAMERAINDEX]

optional arguments:
  -h, --help            show this help message and exit
  --calibrationresult CALIBRATIONRESULT, -c CALIBRATIONRESULT
                        Result from the calibration operation.
  --threshold THRESHOLD, -t THRESHOLD
                        Threshold value to trigger alarm
  --inches
  --videocameraindex VIDEOCAMERAINDEX, -v VIDEOCAMERAINDEX
                        Video camera index
```
**Example**
```shell
python3 social_distancing.py run -c 10385
```

Enjoy.

## Triangular Similarity
The triangle similarity (![](https://latex.codecogs.com/svg.latex?S)) is calculated using the detected
subject width in pixel (![](https://latex.codecogs.com/svg.latex?P)), the known width of the subject 
(![](https://latex.codecogs.com/svg.latex?W)) and the known distance from the camera 
(![](https://latex.codecogs.com/svg.latex?D)) as:

![](https://latex.codecogs.com/svg.latex?\Large&space;S=\frac{P*D}{W})

We can use this data to calculate any later distance (![](https://latex.codecogs.com/svg.latex?D_n))
using the new subject width in pixel (![](https://latex.codecogs.com/svg.latex?P_n)) as:

![](https://latex.codecogs.com/svg.latex?\Large&space;D_n=\frac{W*S}{P_n})

If we replace S from the previous formula

![](https://latex.codecogs.com/svg.latex?\Large&space;D_n=\frac{W*\frac{P*D}{W}}{P_n})

If we approximate the width of any subject as similar

![](https://latex.codecogs.com/svg.latex?\Large&space;D_n=\frac{\frac{W}{W}*P*D}{P_n}=\frac{P*D}{P_n})

So our Calibration number could be defined as

![](https://latex.codecogs.com/svg.latex?\Large&space;C=P*D\Rightarrow&space;D_n=\frac{C}{P_n})

## Known issues

Often OpenCV hangs in the closing phase, so the process must be manually killed.

I'm almost sure it is a dumb problem in my code, but I cannot find the cause. 


## Possible improvements

Assuming that every possible face have the same width is a very bold assumption.
We should find something that OpenCV can reliably detect and, at the same time, is
more universally constant that face width (ie pupil distance). Until we found something
like that, this software can not be considered 100% reliable.
