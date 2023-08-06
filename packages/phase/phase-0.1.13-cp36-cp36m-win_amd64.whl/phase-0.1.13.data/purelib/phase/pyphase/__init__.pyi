"""
        pyPhase is a python wrapper package over I3DR's Phase C++ library.
    """
import phase.pyphase
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "RGBDVideoStream",
    "RGBDVideoWriter",
    "StereoVision",
    "bgr2bgra",
    "bgr2rgba",
    "bgra2rgba",
    "calib",
    "cvMatIsEqual",
    "depth2xyz",
    "disparity2depth",
    "disparity2xyz",
    "flip",
    "getVersionMajor",
    "getVersionMinor",
    "getVersionPatch",
    "getVersionString",
    "normaliseDisparity",
    "processStereo",
    "processStereoFiles",
    "readImage",
    "savePLY",
    "scaleImage",
    "showImage",
    "stereocamera",
    "stereomatcher",
    "types",
    "xyz2depth"
]


class RGBDVideoStream():
    """
    RGBD Video Stream


    Stream RGB and Depth video
    """
    def __init__(self, arg0: str, arg1: str) -> None: ...
    def close(self) -> None: ...
    def getDownsampleFactor(self) -> float: ...
    def getHFOV(self) -> float: ...
    def getHeight(self) -> int: ...
    def getLoadThreadResult(self) -> bool: ...
    @staticmethod
    def getReadThreadResult(*args, **kwargs) -> typing.Any: ...
    def getWidth(self) -> int: ...
    def isFinished(self) -> bool: ...
    def isLoadThreadRunning(self) -> bool: ...
    def isLoaded(self) -> bool: ...
    def isOpened(self) -> bool: ...
    def isReadThreadRunning(self) -> bool: ...
    def load(self) -> bool: ...
    def loadThreaded(self) -> None: ...
    @staticmethod
    def read(*args, **kwargs) -> typing.Any: ...
    def readThreaded(self) -> None: ...
    def restart(self) -> None: ...
    def setDownsampleFactor(self, arg0: float) -> None: ...
    pass
class RGBDVideoWriter():
    """
    RGBD Video Writer


    Write RGB and Depth video
    """
    def __init__(self, arg0: str, arg1: str, arg2: int, arg3: int) -> None: ...
    def add(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> None: ...
    def close(self) -> None: ...
    def getSaveThreadResult(self) -> bool: ...
    def isOpened(self) -> bool: ...
    def isSaveThreadRunning(self) -> bool: ...
    def save(self) -> bool: ...
    def saveThreaded(self) -> None: ...
    pass
class StereoVision():
    """
    Stereo Vision class


    Capture images from stereo camera and process with stereo matcher
    to generate depth. Brings together Stereo Camera and Stereo Matcher classes into
    single class for easy use.
    """
    @staticmethod
    def __init__(*args, **kwargs) -> typing.Any: ...
    def connect(self) -> bool: ...
    def disconnect(self) -> None: ...
    @staticmethod
    def getCalibration(*args, **kwargs) -> typing.Any: ...
    @staticmethod
    def getCamera(*args, **kwargs) -> typing.Any: ...
    def getDownsampleFactor(self) -> float: ...
    def getHFOV(self) -> float: ...
    def getHeight(self) -> int: ...
    @staticmethod
    def getMatcher(*args, **kwargs) -> typing.Any: ...
    @staticmethod
    def getReadThreadResult(*args, **kwargs) -> typing.Any: ...
    def getWidth(self) -> int: ...
    def isCapturing(self) -> bool: ...
    def isConnected(self) -> bool: ...
    def isReadThreadRunning(self) -> bool: ...
    def isValidCalibration(self) -> bool: ...
    @staticmethod
    def read(*args, **kwargs) -> typing.Any: ...
    def setDownsampleFactor(self, arg0: float) -> None: ...
    def setTestImagePaths(self, arg0: str, arg1: str) -> None: ...
    def startCapture(self) -> bool: ...
    def startReadThread(self, timeout: int = 1000, rectify: bool = True) -> None: ...
    def stopCapture(self) -> None: ...
    pass
def bgr2bgra(arg0: numpy.ndarray) -> numpy.ndarray:
    """
    Convert BGR image to BGRA.

    Parameters
    ----------
    bgr : numpy.ndarray
        BGR image to convert

    Returns
    -------
    numpy.ndarray
        BGRA image
    """
def bgr2rgba(arg0: numpy.ndarray) -> numpy.ndarray:
    """
    Convert BGR image to RGBA.

    Parameters
    ----------
    bgr : numpy.ndarray
        BGR image to convert

    Returns
    -------
    numpy.ndarray
        RGBA image
    """
def bgra2rgba(arg0: numpy.ndarray) -> numpy.ndarray:
    """
    Convert BGRA image to RGBA.

    Parameters
    ----------
    bgra : numpy.ndarray
        BGRA image to convert

    Returns
    -------
    numpy.ndarray
        RGBA image
    """
def cvMatIsEqual(arg0: numpy.ndarray, arg1: numpy.ndarray) -> bool:
    """
    Check if two cv::Mat objects are equal.

    Parameters
    ----------
    mat1 : cv::Mat
        First cv::Mat object
    mat2 : cv::Mat
        Second cv::Mat object

    Returns
    -------
    bool
        True if equal
    """
def depth2xyz(arg0: numpy.ndarray, arg1: float) -> numpy.ndarray:
    """
    Calculate Point cloud (xyz) from depth image.

    Parameters
    ----------
    xyz : numpy.ndarray
        Point cloud (xyz)
    hfov : float
        Horizontal field of view (degrees)

    Returns
    -------
    numpy.ndarray
        Point cloud (xyz)
    """
def disparity2depth(arg0: numpy.ndarray, arg1: numpy.ndarray) -> numpy.ndarray:
    """
    Calculate depth image from disparity image.

    Parameters
    ----------
    disparity : numpy.ndarray
        Disparity image
    Q: numpy.ndarray
        Q Matrix from calibration (e.g. 'calibration.getQ()')

    Returns
    -------
    numpy.ndarray
        Depth image
    """
def disparity2xyz(arg0: numpy.ndarray, arg1: numpy.ndarray) -> numpy.ndarray:
    """
    Calculate point cloud (xyz) from disparity image.

    Parameters
    ----------
    disparity : numpy.ndarray
        Disparity image
    Q: numpy.ndarray
        Q Matrix from calibration (e.g. 'calibration.getQ()')

    Returns
    -------
    numpy.ndarray
        Point clouds (xyz)
    """
def flip(arg0: numpy.ndarray, arg1: int) -> numpy.ndarray:
    """
    Flip image horizontally or vertically based on flip code.

    Parameters
    ----------
    image : numpy.ndarray
        Image to flip
    flip_code : int
        Flip code (0 = horizontal, 1 = vertical)

    Returns
    -------
    numpy.ndarray
        Flipped image
    """
def getVersionMajor() -> int:
    pass
def getVersionMinor() -> int:
    pass
def getVersionPatch() -> int:
    pass
def getVersionString() -> str:
    pass
def normaliseDisparity(arg0: numpy.ndarray) -> numpy.ndarray:
    """
    Normalise disparity image.

    Parameters
    ----------
    disparity : numpy.ndarray
        Dispairty image to normalise

    Returns
    -------
    numpy.ndarray
        Normalised disparity image
    """
def processStereo(*args, **kwargs) -> typing.Any:
    pass
def processStereoFiles(*args, **kwargs) -> typing.Any:
    pass
def readImage(arg0: str) -> numpy.ndarray:
    """
    Read image from file.

    Parameters
    ----------
    image_filepath : str
        Filepath of image

    Returns
    -------
    numpy.ndarray
        Image
    """
def savePLY(arg0: str, arg1: numpy.ndarray, arg2: numpy.ndarray) -> bool:
    """
    Save point cloud to PLY file.

    Parameters
    ----------
    ply_filepath : str
        Filepath of PLY file
    xyz : numpy.ndarray
        Point cloud (xyz)
    rgb : numpy.ndarray
        RGB image for point cloud colours

    Returns
    -------
    bool
        True if successful
    """
def scaleImage(arg0: numpy.ndarray, arg1: float) -> numpy.ndarray:
    """
    Scale image to a new size.

    Parameters
    ----------
    image : numpy.ndarray
        Image to scale
    scale_factor : float
        Scale factor to apply to image

    Returns
    -------
    numpy.ndarray
        Scaled image
    """
def showImage(arg0: str, arg1: numpy.ndarray) -> int:
    """
    Display image in GUI window.

    Parameters
    ----------
    window_name : str
        Name of window
    image : numpy.ndarray
        Point cloud (xyz)
    """
def xyz2depth(arg0: numpy.ndarray) -> numpy.ndarray:
    """
    Calculate depth image from point cloud (xyz).

    Parameters
    ----------
    xyz : numpy.ndarray
        Point cloud (xyz)

    Returns
    -------
    numpy.ndarray
        Depth image
    """
