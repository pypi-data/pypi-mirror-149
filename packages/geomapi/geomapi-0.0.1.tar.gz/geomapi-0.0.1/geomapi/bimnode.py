"""
BIMNode - a Python Class to govern the data and metadata of BIM data (Open3D, RDF)
"""
#IMPORT PACKAGES
import open3d as o3d 
import numpy as np 

#IMPORT MODULES
from geomapi.geometrynode import GeometryNode
import geomapi.linkeddatatools as ld

class BIMNode (GeometryNode):
    # class attributes

    def __init__(self): # initialize with a path?
        super().__init__()
        # self.path = None # (string) path of the o3d.mesh geometry
        # self.ifc = None # (string) path to an ifc file => you don't want to store the entire ifc file!
        self.ifcPath = None # (string) path to an ifc file
        # self.ifcElement = None # (string) Don't store an ifcElement in your node. it can't be properly passed around
        # self.pcds = None #(List[URIRef]) => link to other pcd. 
        self.globalId=None # (string) ifc guid of the element e.g. 2DhaSlBmz2puIzqaWbJt0S
        self.className=None #(string) ifcElement class e.g. ifcWall
        #Classification
        self.label = None #(string) ??? (MB)
        # self.meshes = None # (List[URIRef]) => link to other meshes. (MB)
        
        #Geometry
        self.mesh = None # (o3d.mesh) mesh geometry of the ifcElement (MB)
        
        # Monitoring
        self.phase = None # (string) ??? this can't be really extracted from the IFC (MB)
        self.progress = None # (double [0.0;1.0]) percentage of completion
        self.quality = None # ([%LOA30,#LOA20,#LOA10]) inliers Level-of-Accuracy (LOA)
        self.deviation = None # (np.array(4,4)) cartesian transform 
        self.cracks = None # (bool) True if cracks are detected on the image texture

        #Questions
        # is phase and timestamp the same?
        # monenclature
        # where do we store the image masks?
        # do we also need a CAD node?

    def get_data(self)->bool: # deze class is gedeeld met de mesh class
        """
        get o3d.geometry.pointcloud from self.path or self.name
        """
        if hasattr(self,'path') and self.path is not None:
            self.mesh = o3d.io.read_triangle_mesh(self.path)  
            if len(self.mesh.vertices) != 0:
                return True

        elif hasattr(self,'name') and self.name is not None:
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
            self.vertexCount= len(self.mesh.vertices)
            return True
        else:
            print('No geometry found to extract the metadata. Set the geometry first.')
            return False

    # def set_metadata_from_ifc_element(self,ifcElement:ifcopenshell.entity_instance) ->bool: # this fails because ifcElement can't be passed around properly
    #     """
    #     Set BIMNode paramaters from ifcopenshell.ifcElement

    #     Args:
    #         self (BIMNode)
    #         ifcElement (ifcopenshell.ifcElement):  
    #     Returns:
    #         True if success
    #     """   
    #     try:
    #         self.name=ifcElement.Name
    #         self.globalId=ifcElement.GlobalId
    #         self.className=ifcElement.is_a
    #         self.phase= None            
    #         self.guid='{'+str(uuid.uuid1())+'}' 
    #         return True
    #     except:
    #         print('ifcElement parsing error')
    #         return False

    # def set_geometry(self) -> bool:
    #     if not hasattr(self,'mesh') or len(self.mesh.vertices) == 0:
    #         self.mesh=ld.ifc_to_mesh(self.ifcElement)
    #         return True
    #     else:
    #         return False


    # def ifc_to_mesh(self, path):
    #     """
    #     converts ifc geometry to a mesh geometry
    #     """
    #     if not self.ifcElement.get_info().get("Representation") == None: #Check if the product has a geometry representation
    #         modelMesh = MeshNode()
    #         modelMesh.guid = self.guid
    #         modelMesh.name = self.name
    #         modelMesh.sensor = "IFC2x3"

    #         modelMesh.path = path
    #         settings = geom.settings() #Extract the ifcopenshell geometry settings
    #         settings.set(settings.USE_WORLD_COORDS, True) #make sure the global coordinates are enabled

        
    #         shape = geom.create_shape(settings, self.ifcElement) #extract the geometry representation from the model
    #         ios_vertices = shape.geometry.verts #extract the vertices of the IFC geometry
    #         ios_faces = shape.geometry.faces #extract the faces of the IFC geometry

    #         #Group the vertices and faces in a way they can be read by Open3D
    #         grouped_verts = [[ios_vertices[i], ios_vertices[i + 1], ios_vertices[i + 2]] for i in range(0, len(ios_vertices), 3)]
    #         grouped_faces = [[ios_faces[i], ios_faces[i + 1], ios_faces[i + 2]] for i in range(0, len(ios_faces), 3)]

    #         #Convert the lists of grouped vertices and faces to Open3D objects needed to create an Open3D mesh object
    #         vertices = o3d.utility.Vector3dVector(np.asarray(grouped_verts)) #convert verttices to o3d 3D vector elements
    #         triangles = o3d.utility.Vector3iVector(np.asarray(grouped_faces)) #Convert faces to o3d 3D Array element
                                
    #         modelMesh.mesh = o3d.geometry.TriangleMesh(vertices,triangles) #Create the Open3D mesh object
    #         try:
    #             modelMesh.oriented_boundingbox = modelMesh.mesh.get_oriented_bounding_box() #store the oriented_bounding box of the mesh geometry
    #         except:
    #             print("Failed to compute Open3D OrientedBoundingBox")
    #         o3d.io.write_triangle_mesh(modelMesh.path,modelMesh.mesh) # save the TriangleMesh to an obj file
    #         print("EXPORTED MESH")
    #         # except:
    #         #     pass

            
        


    def visualize(self):
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        vis.add_geometry(self.o3d_mesh)
        vis.run()
        vis.destroy_window()

# whats the difference between the ifcopenshell data class and this one? => this one holds the geometry and the link to the ifc
