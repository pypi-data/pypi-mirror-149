"""
MeshNode - a Python Class to govern the data and metadata of mesh data (Open3D, RDF)
"""
#IMPORT PACKAGES
import open3d as o3d 
import numpy as np 

#IMPORT MODULES
from geomapi.geometrynode import GeometryNode
import geomapi.linkeddatatools as ld


SUPPORTED_POINT_FIELDS = {
    "pointCount": "(int)",
    "faceCount": "(int)",
    "mesh": "(o3d.geometry.Mesh)",
}


class MeshNode (GeometryNode):
    # class attributes

    def __init__(self): # initialize with a path?
        #instance attributes        
        super().__init__()
        self.pointCount = None # (int) number of vertices
        self.faceCount = None # (int) number of faces
        self.mesh = None # (o3d.geometry.Mesh) # Open3D point cloud

    def get_data(self)->bool: # deze class is gedeeld met de mesh class
        """
        get o3d.geometry.TriangleMesh from self.path or self.name
        """
        if hasattr(self,'path') and self.path is not None and self.mesh is None:
            self.mesh = o3d.io.read_triangle_mesh(self.path)  
            if len(self.mesh.vertices) != 0:
                return True

        elif hasattr(self,'name') and self.name is not None and self.mesh is None:
            allSessionFilePaths=ld.getListOfFiles(self.sessionPath)
            testOBJPath= self.sessionPath +'\\'+ self.name + '.obj'
            testPLYPath= self.sessionPath + '\\'+ self.name + '.ply'
            if testOBJPath in allSessionFilePaths:
                self.mesh = o3d.io.read_triangle_mesh(testOBJPath)  
                if len(self.mesh.vertices) != 0:
                    self.path=testOBJPath
                    return True
            elif testPLYPath in allSessionFilePaths:
                self.mesh = o3d.io.read_triangle_mesh(testPLYPath)  
                if len(self.mesh.vertices) != 0:
                    self.path=testPLYPath
                    return True
        return False
 
    def set_metadata_from_mesh(self) -> bool:
        if hasattr(self,'mesh') and len(self.mesh.vertices) != 0:
            center=self.mesh.get_center()  
            self.cartesianTransform= np.array([[1,0,0,center[0]],
                                                [0,1,0,center[1]],
                                                [0,0,1,center[2]],
                                                [0,0,0,1]])
            self.cartesianBounds=ld.get_cartesian_bounds(self.mesh)
            self.orientedBounds = ld.get_oriented_bounds(self.mesh)
            self.faceCount= len(self.mesh.triangles)
            self.pointCount= len(self.mesh.vertices)
            return True
        else:
            print('No geometry found to extract the metadata. Set the geometry first.')
            return False
    
    def set_mesh(self, mesh): # this is a strange function (MB)
        self.mesh = mesh
