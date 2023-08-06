
#IMPORT MODULES
from geomapi.geometrynode import GeometryNode
from geomapi.imagenode import ImageNode
import geomapi.linkeddatatools as ld
from geomapi.node import Node

class SessionNode(Node):
    """
    This class stores a full session, including all the images and meshes
    
    Goals:
    - Given a path, import all the linked images, meshes, ect... into a session class
    - Convert non-RDF metadata files (json, xml, ect..) to SessionsNodes and export them to RDF
    - get the boundingbox of the whole session
    - use URIRef() to reference the images ect...
    """

    def __init__(self, path = None):
        """Creates a new Session

        Args:
            path (string, optional): The path of the SessionGraph file. Defaults to None.
        """
        #instance attributes        
        super().__init__()
        self.geometrieNodes = [] # the collection of geometries in this session
        self.imageNodes = [] # the collection of images in this session
        self.bimNodes = [] # the collection of bimObjects in this session
        self.path = path

    def set_imageNodes(self, images):
        """Sets the images of the session to a list of imagenodes

        Args:
            images (List <ImageNode>): A list of Imagenodes
        """
        #check if the list is of imagenodes
        for image in images:
            if (not isinstance(image, ImageNode)):
                return
        # set the imagenodes
        self.imageNodes = images

    def set_geometryNodes(self, geometries):
        """Sets the geometries of the session to a list of geometrynodes

        Args:
            geometries (List <GeometryNode>): A list of geometries
        """
        #check if the list is of imagenodes
        for geometry in geometries:
            if (not isinstance(geometry, GeometryNode)):
                return
        # set the imagenodes
        self.imageNodes = geometries
    
    def get_boundingBox():
        pass

    def test(self, value : str) -> str:
        """Test The functionality

        Args:
            value (str): The strign value to test

        Returns:
            str: The return string
        """
        return "hello " + value
