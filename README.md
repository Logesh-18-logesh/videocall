# WEBSORT VIDEO CALLING #

I modified the library vidstream created by Florian Dedov from NeuralNine to add background removal for the video call streaming.

This repository contains both the modified library and the call.py file to call the library

## HOW DEEPLABV3 MODEL IS USED TO REMOVE BACKGROUND ##

**Semantic Segmentation:** DeepLabv3 identifies the pixels belonging to the person (foreground) and the background.

**Foreground Extraction:** The pixels corresponding to the person are kept, and the rest of the pixels (background) are discarded or made transparent.

**Background Replacement:** The extracted foreground is blended with a new background, allowing for dynamic background changes during video calls.

## HOW TO RUN THE FILE  ## 

1.Install the required libraries:
    > opencv-python
    > opencv-python-headless
    pyautogui \n
    numpy \n
    torch\n
    torchvision\n
    pillow\n
    pyaudio\n
    pickle\n

2.Make sure you have both the vidstream_modified folder and the call.py file in same directory\n

3.In call.py line:69\n
    enter the other device's IP address \n

4.Run the call.py file\n


## HOW THE CODE WORKS: ##
1.It displays the IP address of the device which should be entered in the other device\n
2.Asks what type of background needed\n
3.The selected background will be retrieved from the url and will be given for vidstream library\n
4.The vidstream library is responsible for the streaming \n
5.The cameraclient captures the frames from webcam which will be given to the depplabv3 model for foreground and background identification\n
6.The background will be modified according to the user request and will be sent to the other device for streaming\n
