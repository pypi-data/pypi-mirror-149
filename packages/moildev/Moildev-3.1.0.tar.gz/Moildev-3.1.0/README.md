## Moildev Library

Moildev Library is a collection of functions that support the development of fisheye image applications based on python programing language. You can visit this [documentation](https://github.com/MoilOrg/moildev) to going deep on this library.

### Support cross-platform and multiple python version

This library can support both Linux OS and Windows OS for python version 3.6 ~ 3.10.

### Installation

The easiest  way to install is using PyPI distribution, you can use this command:

```python
pip install moildev
```
or you can download from GitHub [repository](https://github.com/MoilOrg/moildev) and install it by pip command:

```python
cd moildev/
pip install moildev.tar.gz
```

#### 1. Import Library
You can Import library by copy and paste this code to your python file.

```python
from Moildev import Moildev
```
Above code will give you information about moildev version and other information

#### 2. Create object

To create the object from Moildev, you have to provide the parameter. The camera parameter is the result from camera calibration process by MOIL laboratory 

   There 3 way to create object of moildev
   1. Create object using **input keyword arguments**
   2. Create object using **one parameter** with json file format extension 
   3. Create object using **multiple parameter** with json file format extension

**Example**:

```python
# Create object using input keyword arguments
moildev_1 = Moildev(cameraName="Raspi", cameraFov=220, sensorWidth=1.4, sensorHeight=1.4, icx=1298, icy=966, ratio=1,
                    imageWidth=2592, imageHeight=1944, calibrationRatio=4.05, parameter0=0, parameter1=0, parameter2=0,
                    parameter3=0, parameter4=-47.96, parameter5=222.86)
```

**List of camera parameters keyword used to create Moildev objects:**

- cameraName = the name of the camera used
- cameraFov = camera field of view (FOV)
- sensorWidth = size of sensor width
- sensorHeight = size of sensor height
- icx = center image in x-axis
- icy = center image in y-axis
- ratio = the value of the ratio image
- imageWidth = the size of width image
- imageHeight = the size of height image
- calibrationRatio = the value of calibration ratio
- parameter0 .. parameter5= intrinsic fisheye camera parameter get from calibration

*See example [here](https://github.com/MoilOrg/moildev/tree/main/examples/getting_started)*

#### 3. Anypoint image

Python code show bellow:
```python
anypoint_image = moildev.anypoint(image, alpha, beta, zoom, mode=1)
```

- **image**: source image
- **alpha**: the value of alpha
- **beta**: the value of beta
- **zoom**: decimal zoom factor, normally 1..12
- **mode**: mode anypoint view (by default it will be mode 1 and other mode 2)

*See example [here](https://github.com/MoilOrg/moildev/tree/main/examples/anypoint)*

#### 4. Panorama Image

Python code show bellow
```python
panorama_image = moildev.panorama(image, alpha_min, alpha_max)
```

- **image** = the original image  
- **alpha_min** = the minimum alpha 
- **alpha_max** : max of alpha. The recommended vaule is half of camera FOV.

*See example [here](https://github.com/MoilOrg/moildev/tree/main/examples/panorama)*

##### Detail about Moildev library, you can read this [Repository](https://github.com/MoilOrg/moildev)