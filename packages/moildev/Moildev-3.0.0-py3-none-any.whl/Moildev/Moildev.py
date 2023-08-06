import math
import json
import cv2
import numpy as np
from . import MoilCV
import warnings


class Moildev(object):
    def __init__(self, file_camera_parameter=None, camera_type=None, **kwarg):
        """
        This is the initial configuration that you need to provide the camera parameter. The camera parameter is the
        result from calibration camera by MOIL laboratory. before the successive functions can work correctly,
        configuration is necessary in the beginning of program.
        Args:
            file_camera_parameter (): *.json file
            camera_type = the name of the camera type used (use if yore pass the parameter using *.json file)
            cameraName = the name of the camera used
            cameraFov = camera field of view (FOV)
            sensor_width = size of sensor width
            sensor_height = size of sensor height
            Icx = center image in x-axis
            Icy = center image in y-axis
            ratio = the value of the ratio image
            imageWidth = the size of width image
            imageHeight = the size of height image
            calibrationRatio = the value of calibration ratio
            parameter0 .. parameter5= intrinsic fisheye camera parameter get from calibration

        for more detail, please reference https://github.com/MoilOrg/moildev
        """
        super(Moildev, self).__init__()
        self.__alphaToRho_Table = []
        self.__rhoToAlpha_Table = []

        self.__cameraName = None
        self.__cameraFov = None
        self.__sensor_width = None
        self.__sensor_height = None
        self.__Icx = None
        self.__Icy = None
        self.__ratio = None
        self.__imageWidth = None
        self.__imageHeight = None
        self.__calibrationRatio = None
        self.__parameter0 = None
        self.__parameter1 = None
        self.__parameter2 = None
        self.__parameter3 = None
        self.__parameter4 = None
        self.__parameter5 = None

        if file_camera_parameter is None:
            if kwarg == {}:
                print("Pass the argument with camera parameter file with json extension (*.json) "
                      "Or Given list of Parameter,\nsee detail documentation here https://github.com/MoilOrg/moildev")

            else:
                for key, value in kwarg.items():
                    if key == "cameraName":
                        self.__cameraName = value
                    elif key == "cameraFov":
                        self.__cameraFov = value
                    elif key == "sensorWidth":
                        self.__sensor_width = value
                    elif key == "sensorHeight":
                        self.__sensor_height = value
                    elif key == "icx":
                        self.__Icx = value
                    elif key == "icy":
                        self.__Icy = value
                    elif key == "ratio":
                        self.__ratio = value
                    elif key == "imageWidth":
                        self.__imageWidth = value
                    elif key == "imageHeight":
                        self.__imageHeight = value
                    elif key == "calibrationRatio":
                        self.__calibrationRatio = value
                    elif key == "parameter0":
                        self.__parameter0 = value
                    elif key == "parameter1":
                        self.__parameter1 = value
                    elif key == "parameter2":
                        self.__parameter2 = value
                    elif key == "parameter3":
                        self.__parameter3 = value
                    elif key == "parameter4":
                        self.__parameter4 = value
                    elif key == "parameter5":
                        self.__parameter5 = value

                if self.__cameraName is None or \
                        self.__cameraFov is None or \
                        self.__sensor_width is None or \
                        self.__sensor_height is None or \
                        self.__Icx is None or \
                        self.__Icy is None or \
                        self.__ratio is None or \
                        self.__imageWidth is None or \
                        self.__imageHeight is None or \
                        self.__calibrationRatio is None or \
                        self.__parameter0 is None or \
                        self.__parameter1 is None or \
                        self.__parameter2 is None or \
                        self.__parameter3 is None or \
                        self.__parameter4 is None or \
                        self.__parameter5 is None:
                    warnings.warn("You're not passing the complete parameter. please refer to the documentation "
                                  "here https://github.com/MoilOrg/moildev ")
        else:
            self.__setCameraParameter(file_camera_parameter, camera_type)
            if self.__cameraName is not None:
                self.__initAlphaRho_Table()
                self.__importMoildev()

    def __setCameraParameter(self, parameter, cameraType):
        """
        Set up the configuration of the camera parameter
        Args:
            parameter (): the *.json file
            cameraType (): type of the camera

        Returns:
            None
        """
        with open(parameter) as f:
            data = json.load(f)
            if cameraType in data.keys():
                self.__cameraName = data[cameraType]["cameraName"]
                self.__cameraFov = data[cameraType]["cameraFov"] if "cameraFov" in data[cameraType].keys() else 220
                self.__sensor_width = data[cameraType]['cameraSensorWidth']
                self.__sensor_height = data[cameraType]['cameraSensorHeight']
                self.__Icx = data[cameraType]['iCx']
                self.__Icy = data[cameraType]['iCy']
                self.__ratio = data[cameraType]['ratio']
                self.__imageWidth = data[cameraType]['imageWidth']
                self.__imageHeight = data[cameraType]['imageHeight']
                self.__calibrationRatio = data[cameraType]['calibrationRatio']
                self.__parameter0 = data[cameraType]['parameter0']
                self.__parameter1 = data[cameraType]['parameter1']
                self.__parameter2 = data[cameraType]['parameter2']
                self.__parameter3 = data[cameraType]['parameter3']
                self.__parameter4 = data[cameraType]['parameter4']
                self.__parameter5 = data[cameraType]['parameter5']

            else:
                if "cameraName" in data.keys() and cameraType is None:
                    with open(parameter) as file:
                        data = json.load(file)
                        self.__cameraName = data["cameraName"]
                        self.__cameraFov = data["cameraFov"] if "cameraFov" in data.keys() else 220
                        self.__sensor_width = data['cameraSensorWidth']
                        self.__sensor_height = data['cameraSensorHeight']
                        self.__Icx = data['iCx']
                        self.__Icy = data['iCy']
                        self.__ratio = data['ratio']
                        self.__imageWidth = data['imageWidth']
                        self.__imageHeight = data['imageHeight']
                        self.__calibrationRatio = data['calibrationRatio']
                        self.__parameter0 = data['parameter0']
                        self.__parameter1 = data['parameter1']
                        self.__parameter2 = data['parameter2']
                        self.__parameter3 = data['parameter3']
                        self.__parameter4 = data['parameter4']
                        self.__parameter5 = data['parameter5']

                else:
                    warnings.warn("Please Check your parameter file. \n"
                                  "If file has multiple camera parameter, typing the name of camera!!\n"
                                  "see detail documentation here https://github.com/MoilOrg/moildev\n"
                                  "or you can email to 'haryanto@o365.mcut.edu.tw'")
    
    @classmethod
    def version(cls):
        """
        Showing the version of the library and the new feature updated.

        Returns:
            Moildev version
        """
        MoilCV.version()

    def __initAlphaRho_Table(self):
        """
        Create list for initial alpha to rho(height image).

        Returns:
            Initial alpha and rho table.
        """
        for i in range(1800):
            alpha = i / 10 * math.pi / 180
            self.__alphaToRho_Table.append(
                (self.__parameter0 *
                 alpha *
                 alpha *
                 alpha *
                 alpha *
                 alpha *
                 alpha +
                 self.__parameter1 *
                 alpha *
                 alpha *
                 alpha *
                 alpha *
                 alpha +
                 self.__parameter2 *
                 alpha *
                 alpha *
                 alpha *
                 alpha +
                 self.__parameter3 *
                 alpha *
                 alpha *
                 alpha +
                 self.__parameter4 *
                 alpha *
                 alpha +
                 self.__parameter5 *
                 alpha) *
                self.__calibrationRatio)
            i += 1

        i = 0
        index = 0
        while i < 1800:
            while index < self.__alphaToRho_Table[i]:
                self.__rhoToAlpha_Table.append(i)
                index += 1
            i += 1

        while index < 3600:
            self.__rhoToAlpha_Table.append(i)
            index += 1

    def getCameraName(self):
        """
        Get camera name.

        Returns:
            Camera name (string)
        """
        return self.__cameraName

    def getCameraFov(self):
        """
        Get Field of View Camera.

        Returns:
            FoV camera (int)
        """
        return self.__cameraFov

    def getIcx(self):
        """
        Get center image from width image.

        Returns:
            Image center X (int)
        """
        return self.__Icx

    def getIcy(self):
        """
        Get center image from height image.

        Returns:
            Image center Y(int)
        """
        if self.__Icy is not None:
            return self.__Icy

    def getImageWidth(self):
        """
        Get the size width of the image.

        Returns:
            image width(int)
        """
        return self.__imageWidth

    def getImageHeight(self):
        """
        Get the size height of the image.

        Returns:
            image height(int)
        """
        return self.__imageHeight

    def __importMoildev(self):
        """
        Create moildev instance from Moildev SDK share object library.

        Returns:
            Moildev object (private attribute for this class)
        """
        self.__moildev = MoilCV.MoilCV(
            self.__cameraName,
            self.__sensor_width,
            self.__sensor_height,
            self.__Icx,
            self.__Icy,
            self.__ratio,
            self.__imageWidth,
            self.__imageHeight,
            self.__calibrationRatio,
            self.__parameter0,
            self.__parameter1,
            self.__parameter2,
            self.__parameter3,
            self.__parameter4,
            self.__parameter5)
        self.__map_x = np.zeros(
            (self.__imageHeight,
             self.__imageWidth),
            dtype=np.float32)
        self.__map_y = np.zeros(
            (self.__imageHeight,
             self.__imageWidth),
            dtype=np.float32)
        self.__res = self.__create_map_result_image()

    def __create_map_result_image(self):
        """
        Create Maps image from zeroes matrix for result image.

        Returns:
            Zeroes matrix same size with original image to stored data from result image.
        """
        size = self.__imageHeight, self.__imageWidth, 3
        return np.zeros(size, dtype=np.uint8)

    def getAnypointMaps(self, alpha, beta, zoom, mode=1):
        """The purpose is to generate a pair of X-Y Maps for the specified alpha, beta and zoom parameters,
        the result X-Y Maps can be used later to remap the original fisheye image to the target angle image.

        Args:
            alpha (): value of zenithal distance(float).
            beta (): value of azimuthal distance based on cartography system(float)
            zoom (): value of zoom(float)
            mode (): selection anypoint mode(1 or 2)

        Returns:
            mapX: the mapping matrices X
            mapY: the mapping matrices Y

        Examples:
            please reference: https://github.com/MoilOrg/moildev
        """
        if mode == 1:
            if beta < 0:
                beta = beta + 360
            if alpha < -90 or alpha > 90 or beta < 0 or beta > 360:
                alpha = 0
                beta = 0

            else:
                alpha = -90 if alpha < -90 else alpha
                alpha = 90 if alpha > 90 else alpha
                beta = 0 if beta < 0 else beta
                beta = 360 if beta > 360 else beta
            self.__moildev.AnyPointM(
                self.__map_x, self.__map_y, alpha, beta, zoom)

        else:
            if alpha < - 90 or alpha > 90 or beta < -90 or beta > 90:
                alpha = 0
                beta = 0

            else:
                alpha = -90 if alpha < -90 else alpha
                alpha = 90 if alpha > 90 else alpha
                beta = -90 if beta < -90 else beta
                beta = 90 if beta > 90 else beta
            self.__moildev.AnyPointM2(
                self.__map_x, self.__map_y, alpha, beta, zoom)
        return self.__map_x, self.__map_y

    def getPanoramaMaps(self, alpha_min, alpha_max):
        """
        To generate a pair of X-Y Maps for alpha within 0 ... alpha_max degree, the result X-Y Maps can be used later
        to generate a panorama image from the original fisheye image.

        Args:
            alpha_min (): the minimum alpha degree given
            alpha_max (): the maximum alpha degree given. The recommended value is half of camera FOV. For example, use
                          90 for a 180 degree fisheye images and use 110 for a 220 degree fisheye images.

        Returns:
            mapX: the mapping matrices X
            mapY: the mapping matrices Y

        Examples:
            please reference: https://github.com/MoilOrg/moildev
        """
        self.__moildev.Panorama(
            self.__map_x,
            self.__map_y,
            alpha_min,
            alpha_max)
        return self.__map_x, self.__map_y

    def anypoint(self, image, alpha, beta, zoom, mode=1):
        """
        Generate anypoint view image. for mode 1, the result rotation is betaOffset degree rotation around the
        Z-axis(roll) after alphaOffset degree rotation around the X-axis(pitch). for mode 2, The result rotation
        is thetaY degree rotation around the Y-axis(yaw) after thetaX degree rotation around the X-axis(pitch).

        Args:
            image (): source image given
            alpha (): the alpha offset that corespondent to the pitch rotation
            beta (): the beta offset that corespondent to the yaw rotation
            zoom (): decimal zoom factor, normally 1..12
            mode (): the mode view selected

        Returns:
            anypoint image

        Examples:
            please reference: https://github.com/MoilOrg/moildev
        """
        map_x, map_y = self.getAnypointMaps(alpha, beta, zoom, mode)
        image = cv2.remap(image, map_x, map_y, cv2.INTER_CUBIC)
        return image

    def panorama(self, image, alpha_min, alpha_max):
        """
        The panorama image centered at the 3D direction with alpha = iC_alpha_degree and beta = iC_beta_degree.

        Args:
            image: image source given
            alpha_min:
            alpha_max:

        Returns:
            Panorama view image

        Examples:
            please reference: https://github.com/MoilOrg/moildev
        """
        map_x, map_y = self.getPanoramaMaps(alpha_min, alpha_max)
        image = cv2.remap(image, map_x, map_y, cv2.INTER_CUBIC)
        return image

    def PanoramaM_Rt(self, alpha_max, alpha, beta):
        """
        To generate a pair of X-Y Maps for alpha within 0..alpha_max degree, the result X-Y Maps can be used later
        to generate a panorama image from the original fisheye image. The panorama image centered at the 3D
        direction with alpha = iC_alpha_degree and beta = iC_beta_degree.

        Args:
            . alpha_max : max of alpha. The recommended value is half of camera FOV. For example, use
              90 for a 180 degree fisheye images and use 110 for a 220 degree fisheye images.
            . alpha : alpha angle of panorama center.
            . beta : beta angle of panorama center.

        Returns:
            New mapX and mapY.

        Examples:
            please reference: https://github.com/MoilOrg/moildev
        """
        self.__moildev.PanoramaM_Rt(
            self.__map_x, self.__map_y, alpha_max, alpha, beta)
        return self.__map_x, self.__map_y

    def reverseImage(self, image, alpha_max, alpha, beta):
        """
        To generate the image reverse image from panorama that can change the focus direction from the original
        images. The panorama reverse image centered at the 3D direction with alpha_max = max of alpha and beta =
        iC_beta_degree.

        Args:
            image: source image given
            alpha_max: the value of alpha_max. is half of camera FOV. For example, use
                        90 for a 180 degree fisheye images and use 110 for a 220 degree fisheye images.
            alpha: the value of alpha degree
            beta: the value of alpha degree

        Returns:
            the reverse image

        Examples:
            please reference: https://github.com/MoilOrg/moildev
        """
        self.__moildev.PanoramaM_Rt(
            self.__map_x, self.__map_y, alpha_max, alpha, beta)
        result = cv2.remap(image, self.__map_x, self.__map_y, cv2.INTER_CUBIC)
        self.__moildev.revPanorama(result, self.__res, alpha_max, beta)
        return self.__res

    def getAlphaFromRho(self, rho):
        """
        Get the alpha from rho image.
        Args:
            rho: the value of rho given

        Returns:
            alpha
        """
        if rho >= 0:
            return self.__rhoToAlpha_Table[rho] / 10
        else:
            return -self.__rhoToAlpha_Table[-rho] / 10

    def getRhoFromAlpha(self, alpha):
        """
        Get rho image from alpha given.

        Args:
            alpha: the value of alpha given

        Returns:
            rho image

        """
        return self.__alphaToRho_Table[round(alpha * 10)]

    def getAlphaBeta(self, coordinateX, coordinateY, mode=1):
        """
        Get the alpha beta from specific coordinate image.

        Args:
            coordinateX:
            coordinateY:
            mode:

        Returns:
            alpha, beta

        Examples:
            please reference: https://github.com/MoilOrg/moildev
        """
        delta_x = coordinateX - self.__Icx
        delta_y = -(coordinateY - self.__Icy)
        if mode == 1:
            r = round(math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2)))
            alpha = self.getAlphaFromRho(r)
            if coordinateX == self.__Icy:
                angle = 0
            else:
                angle = (math.atan2(delta_y, delta_x) * 180) / math.pi
            beta = 90 - angle
        else:
            alpha = self.getAlphaFromRho(delta_y)
            beta = self.getAlphaFromRho(delta_x)
        return alpha, beta
