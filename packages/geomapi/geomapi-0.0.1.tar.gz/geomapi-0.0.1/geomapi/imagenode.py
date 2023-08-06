"""
ImageNode - a Python Class to govern the data and metadata of image data (JPG,PNG,XML,XMP)
"""
#IMPORT PACKAGES
import xml.etree.ElementTree as ET

import cv2
import PIL
import PIL.Image as PILimage
from PIL import ImageDraw, ImageEnhance, ImageFont
from PIL.ExifTags import GPSTAGS, TAGS

#IMPORT MODULES
import geomapi.linkeddatatools as ld
from geomapi.node import Node

SUPPORTED_POINT_FIELDS = {
    "xResolution": "(float)",
    "yResolution": "(float)",
    "resolutionUnit": "(float)",
    "imageWidth": "(float) number of pixels",
    "imageHeight": "(float) number of pixels",
    "focalLength35mm": "(float) focal length in mm",
    "principalPointU": "(float) u parameter of principal point (mm)",
    "principalPointV": "(float) v parameter of principal point (mm)",
    "distortionCoeficients": "(float[])",
    "features": "(float[])",
}

class ImageNode(Node):
    # class attributes
    
    def __init__(self):
        super().__init__()
        self.xResolution = None # (Float) 
        self.yResolution = None # (Float) 
        self.resolutionUnit = None # (string)
        self.imageWidth = None # (int) number of pixels
        self.imageHeight = None  # (int) number of pixels
        self.focalLength35mm = None # (Float) focal length in mm
        self.principalPointU= None # (Float) u parameter of principal point (mm)
        self.principalPointV= None # (Float) v parameter of principal point (mm)
        self.distortionCoeficients = None # (Float[])         
        
        #data
        self.img= None # (OpenCV) image
        self.exifData=None # (EXIF) optional exif data
        self.features2d= None #o3d.registration.Feature() # http://www.open3d.org/docs/0.9.0/python_api/open3d.registration.Feature.html

        #Questions
        # where do we store the image masks?
        # where do we store depth maps?
        # where do we store undistorted images?
        # where do we store photogrammetric reconstructions => cartesian transform of the node?
        # where do we store polygon selections + classifications?
        # where do we store image classifications


    def get_data(self):
        """
        get cv2 image
        """
        if self.path is not None:
            self.img = cv2.imread(self.path)  
            return True
        return False

    def get_exif_data(self):
        """Returns a dictionary from the exif data of an Image item. Also
        converts the GPS Tags"""
        exifData = {}
        info = self.img._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]

                    exifData[decoded] = gps_data
                else:
                    exifData[decoded] = value
            self.exifData=exifData        

    def set_exif_data(self):
        self.timestamp=ld.get_if_exist(self.exifData, "DateTime")
        self.xResolution=ld.get_if_exist(self.exifData,"XResolution")
        self.yResolution=ld.get_if_exist(self.exifData,"YResolution")
        self.resolutionUnit=ld.get_if_exist(self.exifData,"ResolutionUnit")
        self.imageWidth=ld.get_if_exist(self.exifData,"ExifImageWidth")
        self.imageHeight=ld.get_if_exist(self.exifData,"ExifImageHeight")
        
        if 'GPSInfo' in self.exifData:
            gps_info = self.exifData["GPSInfo"]
            if gps_info is not None:
                # self.GlobalPose=GlobalPose # (structure) SphericalTranslation(lat,long,alt), Quaternion(qw,qx,qy,qz)
                self.geospatialTransform=[ld.get_if_exist(gps_info, "GPSLatitude"), ld.get_if_exist(gps_info, "GPSLongitude"),ld.get_if_exist(gps_info, "GPSAltitude")]

    def read_img_xmp(self , xmp_path : str):
        mytree = ET.parse(xmp_path)
        root = mytree.getroot()       

        for img_description in root.iter('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description'):
            self.focalLength35mm=float(img_description.attrib['{http://www.capturingreality.com/ns/xcr/1.1#}FocalLength35mm'])
            self.principalPointU=float(img_description.attrib['{http://www.capturingreality.com/ns/xcr/1.1#}PrincipalPointU'])
            self.principalPointV=float(img_description.attrib['{http://www.capturingreality.com/ns/xcr/1.1#}PrincipalPointV'])

            rotationnode=img_description.find('{http://www.capturingreality.com/ns/xcr/1.1#}Rotation')
            if rotationnode is not None:
                rotationMatrix=ld.string_to_rotation_matrix(rotationnode.text)
                self.cartesianTransform=rotationMatrix

            positionnode=img_description.find('{http://www.capturingreality.com/ns/xcr/1.1#}Position')
            if positionnode is not None:
                self.cartesianTransform[0,3]=float(positionnode.text.split(' ')[0])
                self.cartesianTransform[1,3]=float(positionnode.text.split(' ')[1])
                self.cartesianTransform[2,3]=float(positionnode.text.split(' ')[2])

            coeficientnode=img_description.find('{http://www.capturingreality.com/ns/xcr/1.1#}DistortionCoeficients')
            if coeficientnode is not None:
                self.distortionCoeficients=ld.string_to_array(coeficientnode.text)     
