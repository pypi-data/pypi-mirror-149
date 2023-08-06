"""
PointCloudNode - a Python Class to govern the data and metadata of point cloud data (Open3D, RDF)
"""
#IMPORT PACKAGES
from ast import Try
from logging import NullHandler
from pathlib import Path
from typing import Type
from urllib.request import ProxyBasicAuthHandler
import xml.etree.ElementTree as ET
from xmlrpc.client import Boolean 
import open3d as o3d 
# from pathlib import Path # https://docs.python.org/3/library/pathlib.html
import numpy as np 
import os
import sys
import math
import rdflib #https://rdflib.readthedocs.io/en/stable/
# from rdflib.serializer import Serializer #pip install rdflib-jsonld https://pypi.org/project/rdflib-jsonld/
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD
import pye57 #conda install xerces-c  =>  pip install pye57
from scipy.spatial.transform import Rotation as R

#IMPORT MODULES
import geomapi.geometrynode 
import geomapi.linkeddatatools as ld

SUPPORTED_POINT_FIELDS = {
    "vertexCount": "(int)",
    "faceCount": "(int)",
    "o3dPointcloud": "(o3d.geometry.PointCloud)",
}


class PointCloudNode (geomapi.geometrynode.GeometryNode):
    # class attributes

    def __init__(self): # initialize with a path?
        super().__init__() 
        self.pointCount = None # (int) number of vertices
        self.labels = None # (int[]) list of point classificaitons
        self.labelInfo = None # (string) relation between labels and classes, models used, training, etc.
        self.classification = None # (string) class of the node
        
        #data
        self.pcd = None # (o3d.geometry.PointCloud) # Open3D point cloud
        # self.e57Pointcloud = None # raw E57 data file => Do we really want to retain this link?
        # self.e57xmlNode = None # (xml.etree.ElementTree)
        self.e57XmlPath = None # (string) full path to the e57 xml file
        self.e57Path = None # (string) full path to e57 file
        self.e57Index = None # (int) index of scan in e57 file
        self.e57Image = None # (URIRef) pointer to ImageNode (xml.etree.ElementTree) 

        #Questions
        # where do we store normals?
        # where do we selections + classifications? => subnodes

    def visualize(self):
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        vis.add_geometry(self.o3d_mesh)
        vis.run()
        vis.destroy_window()
# the e57 images should be defined as imagenodes and a link should be added to the graph

    def get_data(self)->bool:
        """
        get o3d.geometry.pointcloud from self.path or self.name
        """
        if hasattr(self,'path') and self.path is not None and self.pcd is None:
            self.pcd = o3d.io.read_point_cloud(self.path)
            if len(self.pcd.points) != 0:
                return True

        if hasattr(self,'e57Path') and self.e57Path is not None and hasattr(self,'e57Index') and self.e57Index is not None and self.pcd is None:
            e57 = pye57.E57(self.e57Path)   
            e57scan = e57.read_scan_raw(self.e57Index) 
            self.pcd=ld.e57_to_pcd(e57scan)
            if len(self.pcd.points) != 0:
                return True

        elif hasattr(self,'name') and self.name is not None and self.pcd is None:
            allSessionFilePaths=ld.getListOfFiles(self.sessionPath)
            testE57Path= self.sessionPath +'\\'+ self.name + '.e57'
            testPcdPath= self.sessionPath + '\\'+ self.name + '.pcd'
            if testE57Path in allSessionFilePaths:
                e57 = pye57.E57(testE57Path)   
                e57scan = e57.read_scan_raw(self.e57Index) 
                self.pcd=ld.e57_to_pcd(e57scan)
                if len(self.pcd.points) != 0:
                    return True
            elif testPcdPath in allSessionFilePaths:
                self.pcd = o3d.io.read_point_cloud(testPcdPath)
                if len(self.pcd.points) != 0:
                    return True
        return False
    
    def set_pcd_path_from_e57(self):
        if hasattr(self,'name') and hasattr(self, 'e57Path'):
            folder=ld.get_folder(self.e57Path)
            self.path=folder+'\\'+self.name+'.pcd'
        else:
            pass

    def set_from_pcd(self)->bool:
        """
        set PointCloudNode Metadata from PCD object
        """
        if hasattr(self,'pcd') and len(self.pcd.points) != 0:
            center=self.pcd.get_center()  
            self.cartesianTransform= np.array([[1,0,0,center[0]],
                                                [0,1,0,center[1]],
                                                [0,0,1,center[2]],
                                                [0,0,0,1]])
            self.cartesianBounds=ld.get_cartesian_bounds(self.pcd)
            self.orientedBounds = ld.get_oriented_bounds(self.pcd)
            self.vertexCount= len(self.pcd.points)
            return True
        else:
            print('No geometry found to extract the metadata. Set the geometry first.')
            return False

    def set_from_e57_header(self, header : pye57.scan_header.ScanHeader)->bool: 
        """
        set PointCloudNode Metadata from E57 ScanHeader object
        """
        try:
            self.pointCount=header.point_count
            self.guid=header["guid"].value()
            r=header.rotation_matrix
            t=header.translation
            self.cartesianTransform=np.array([[r[0,0],r[0,1],r[0,2],t[0]],
                                            [r[1,0],r[1,1],r[1,2],t[1]],
                                            [r[2,0],r[2,1],r[2,2],t[2]],
                                            [0,0,0,1]])
            c=header.cartesianBounds
            self.cartesianBounds=np.array([c["xMinimum"].value(),
                                            c["xMaximum"].value(), 
                                            c["yMinimum"].value(),
                                            c["yMaximum"].value(),
                                            c["zMinimum"].value(),
                                            c["zMaximum"].value()])            
            return True
        except:
            print("Parsing e57 header failed (maybe some missing metadata?)!")
            return False      

    def set_from_e57_xml_node(self, e57xml : ET.Element) -> bool: 
        """
        set PointCloudNode Metadata from E57 XML object
        """
        self.guid=e57xml.find('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}guid').text
        # self.name=e57xml.find('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}name').text.replace(' ','_')

        #cartesianBounds
        cartesianBoundsnode=e57xml.find('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}cartesianBounds') 
        if cartesianBoundsnode is not None:
            try:
                cartesianBounds=np.array([ld.xml_to_float(cartesianBoundsnode[0].text),
                                        ld.xml_to_float(cartesianBoundsnode[1].text),
                                        ld.xml_to_float(cartesianBoundsnode[2].text),
                                        ld.xml_to_float(cartesianBoundsnode[3].text),
                                        ld.xml_to_float(cartesianBoundsnode[4].text),
                                        ld.xml_to_float(cartesianBoundsnode[5].text)])
                cartesianBounds=cartesianBounds.astype(np.float)
                cartesianBounds=np.nan_to_num(cartesianBounds)
            except:
                cartesianBounds=np.array([0.0,0.0,0.0,0.0,0.0,0.0])
        self.cartesianBounds=cartesianBounds

        #POSE
        posenode=e57xml.find('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}pose')
        if posenode is not None:
            rotationnode=posenode.find('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}rotation')
            if rotationnode is not None:               
                try:
                    quaternion=np.array([ld.xml_to_float(rotationnode[3].text),
                                        ld.xml_to_float(rotationnode[0].text),
                                        ld.xml_to_float(rotationnode[1].text),
                                        ld.xml_to_float(rotationnode[2].text)])
                    quaternion=quaternion.astype(np.float)   
                    quaternion=np.nan_to_num(quaternion)                
                except:
                    quaternion=np.array([0,0,0,1])
                r = R.from_quat(quaternion)
                rotationMatrix=r.as_matrix()

            translationnode=posenode.find('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}translation')
            if translationnode is not None: 
                try:
                    translationVector= np.array([ld.xml_to_float(translationnode[0].text),
                                                ld.xml_to_float(translationnode[1].text),
                                                ld.xml_to_float(translationnode[2].text)])
                    translationVector=translationVector.astype(np.float)
                    translationVector=np.nan_to_num(translationVector)       
                except:
                    translationVector=np.array([0.0,0.0,0.0])
            self.cartesianTransform=ld.rotation_and_translation_to_transformation_matrix(rotationMatrix,translationVector)
        # SET POSE FROM cartesianBounds
        elif self.cartesianBounds is not None:            
            self.cartesianTransform=ld.cartesian_bounds_to_cartesian_transform(self.cartesianBounds)

        pointsnode=e57xml.find('{http://www.astm.org/COMMIT/E57/2010-e57-v1.0}points')
        if not pointsnode is None:
            self.pointCount=int(pointsnode.attrib['recordCount'])

