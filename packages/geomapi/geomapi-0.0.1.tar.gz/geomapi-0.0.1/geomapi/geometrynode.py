"""
GeometryNode - a Python Class to govern the data and metadata of geometric data (Mesh, BIM, PCD)
"""

#IMPORT MODULES
from geomapi.node import Node

class GeometryNode (Node):
    # class attributes

    def __init__(self): # this class seems a bit empty?
        #instance attributes        
        super().__init__()
        self.cartesianBounds=None     # (nparray [6x1]) [xMin,xMax,yMin,yMax,zMin,zMax]
        self.features3d= None #o3d.registration.Feature() # http://www.open3d.org/docs/0.9.0/python_api/open3d.registration.Feature.html
        
