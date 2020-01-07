
## Buid a object tracking robot with SunFounder Smart Video Car Kit for Raspberry Pi


### About this project:
This project is accomplished by a group of students from CSYE7220 DevOps class in Fall 2019 semester at Northeastern University Our goal is to build a robot with object recgonizing and tracking functionality, containerize and deploy the brain of it on cloud so everybody can reuse our resource to build their own robot.

This entire code set is divided into two part, server and client. The server code is provided by [Sunfounder_PiCar_V](https://github.com/sunfounder/SunFounder_PiCar-V) which runs under Python 2 and Django 1.9, and the client code developed by us runs with Python 3 and OpenCV 4.0.
Server side runs on Raspberry Pi, and you can run the client side on Windows and Linux (Haven't test on Mac.).
Also, you can control the car via web browser. Even though its not that better, but it works. 

----------------------------------------------
### Robot assembly:
This project is using the [SunFounder Smart Video Car Kit V2.0 for Raspberry Pi](https://www.amazon.com/gp/product/B06XWSVLL8/ref=ox_sc_act_title_4?smid=ADHH624DX2Q66&psc=1)
We have documented the entire process of robot assemblying and testing here, see [Duck Robot Manual.pdf](https://bitbucket.org/devopsduckbot/csye7220_duckbot/src/7501b5a934d1/Duck%20Robot%20Manual.pdf?at=vision_client)

----------------------------------------------
### Client Environment Configuration:

#### 1. Manual Install
With Anaconda installed, go to your Anaconda Prompt and follow the steps:

    conda create -n duck_robot tensorflow

    conda activate duck_robot 

    conda install -c conda_forge opencv

    pip install imutils

    conda install CMake

    pip install dlib

    pip install requests
    
#### 2. Using Containerized environment
Go to https://anaconda.org/anning1995/environments

Select duck_robot environment, click the Files tab, and under the Names field click object_chasing_robot.yml to download.

Then using the Terminal or an Anaconda Prompt:
    
    conda env create -f object_chasing_robot.yml

Then go to ./client, run:

    python client_track.py -l <--label> {-u <--url> -t <--track> -c <--confidence>}
        --help for more information

----------------------------------------------
### Get it running:
#### 1. Get the robot server up and running:
First we need to bring up the Django server. To do that we need to first find out the IP address of the robot by [private network IP scanner](https://www.advanced-ip-scanner.com/).
After get your robot connect to your network and get the IP address, go to your command line or terminal:
    
    ssh pi@[IP address of yur robot]
    
It will ask for SSH credential if it's not set up in SD card. The default password should be "raspberry".

Then go to directory: ~/Sunfounder_PiCar-V/remote_control and run:

    ./start

It will show you the server is running after few seconds. If you want to stop it simply press ctrl + C

#### 1. Get the client side up and running:
After configure your anaconda environment on the cient side, activate your environment by running:

    conda activate [your environment name for the robot]

Then download the latest client code and run:
    
    python client_track.py -u [IP address of the robot server] -l [class label you are interested in detecting]

For more accepted arguments, see Toubleshooting section below.

----------------------------------------------
### Troubleshooting:
#### 1. Robot issue:
After assembling correctly, if you can't ssh into the robot, please:
    1. Boot the RPI, make sure the RED LED is ON. If not, recharge the bettery, make sure the power cable is connected correctly and reboot.
    2. Boot the RPI, make sure the green LED is BLINKING. If not, check if the SD card is inserted correctly with system image burnt into it.
    3. If the LED lights are performing normally, check if the SSH file and Network config file has been placed in right directory and the network name and credential setting fit the network you are using.

#### 2. Environment issue:
If manual install does not work, it might because the version of the packages installed with anaconda has been changed. Please try to install the environment from https://anaconda.org/anning1995/environments.

#### 3. Code issue:
To run the object tracking application running, you are supposed to run client_track.py with arguments below:
    -u or --url : IP address of the robot server in your private network, default to be http://192.168.43.58
    -l or --label : class label you are interested in detecting + tracking, such as person
    -t or --track : determine if yoiu want to enable the tracking functionality, default to be 1 which means enabled
    -c or --confidence : the confidencial threashold you want to use for oject detection, default to be 0.8

#### 4. Other issue:
If there is any other problem happens during the robot assembling or running, please feel free to contact me at ye.an@husky.neu.edu.

===================

