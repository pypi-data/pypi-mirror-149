"""
Node - a Python Class to govern the data and metadata of remote sensing data (pcd, images, meshes, orthomozaik)
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
# import pye57 #conda install xerces-c  =>  pip install pye57
from scipy.spatial.transform import Rotation as R

#IMPORT MODULES
import geomapi.utils
import geomapi.linkeddatatools as ld

SUPPORTED_POINT_FIELDS = {
    "name": "(string)",
    "guid": "(string)",
    "sessionName": "(string)",
    "timestamp": "(string)",
    "sensor": "(string)",
    "CartesianBounds": "(float nparray [6x1) [xMin,xMax,yMin,yMax,zMin,zMax]",
    "accuracy": "(float)",
    "cartesianTransform": "(float nparray [4x4]) 3D transform including location, scale and rotation",
    "geospatialTransform": "(float nparray [3x1]) ellipsoidal WGS84 coordinate system {latitude (+=East), longitude(+=North), altitude (+=Up)}",
    "coordinateSystem": "(string) Lambert72, Lambert2008, geospatial-wgs84, local",
    "path": "(string) relative path to the RDF graph folder",
    "graph": "(Graph) RDFLIB ",
    }

class Node:

    def __init__(self):
        #instance attributes
        self.name = None          # (string) name of the node
        self.guid = None          # (string) guid of the node
        self.sessionName = None   # (string) session node name
        self.timestamp = None     # (string) e.g. 2020-04-11 12:00:01 UTC
        self.sensor = None        # (string) sensor information P30, BLK, Hololens2, CANON, etc.

        #Geometry
        self.cartesianBounds=None     # (nparray [6x1]) [xMin,xMax,yMin,yMax,zMin,zMax]
        self.orientedBounds = None    # (nparray [8x3]) 
        self.accuracy = None          # (float) metric data accuracy e.g. 0.05m

        #Coordinate system information
        self.cartesianTransform=None  # (nparray [4x4]) 3D transform including location, scale and rotation 
        self.geospatialTransform=None # (nparray [3x1]) ellipsoidal WGS84 coordinate system {latitude (+=East), longitude(+=North), altitude (+=Up)}
        self.coordinateSystem = None  # (string) coordinate system i.e. Lambert72, Lambert2008, geospatial-wgs84, local + reference /offset
  
        #paths
        self.path = None # (string) absolute path to the node
        self.sessionPath =None # (string) absolute path to the session folder
        self.graphPath= None # (string) absolute path to the folder with the RDF graph 
        
        #metadata
        self.graph = None # (Graph) rdflib

        #Relations
        self.hasPcd = None #(List[URIRef]) link to observed pcd of the node (MB)
        self.hasMesh = None #(List[URIRef]) link to observed meshes of the node (MB)
        self.hasOrtho = None #(List[URIRef]) link to observed orthomosaics of the node (MB)
        self.hasImg = None #(List[URIRef]) link to observed images of the node (MB)
        self.hasCAD= None #do we want to establish such a link?
        self.hasBIM=None #(List[URIRef]) link to BIMNodes that also represent this node (MB)


    def to_graph(self):
        """
        Register all parameters to RDF graph
        """
        # if graph does not exist => create graph
        if self.graph is None:
            g=Graph()
            # Create an RDF URI node to use as the subject for multiple triples
            if self.name is None:
                self.name = 'myNode'
            subject = URIRef('http://'+ self.name.replace(' ','_')) 
            g.add((subject, RDF.type, Literal(str(type(self)))))

            ld.bind_ontologies(g)
        # if graph exists => add triples
        else:
            g=self.graph
            subject=next(g.subjects()) 

        # enumerate attributes in node and write them to triples
        attributes = geomapi.utils.get_variables_in_class(self)
        attributes=ld.clean_attributes_list(attributes)        
        pathlist=ld.get_paths_in_class(self)
              
        for attribute in attributes: 
            value=getattr(self,attribute)
            if value is not None and attribute not in pathlist:
                #find appropriete RDF URI
                predicate = ld.match_uri(attribute)
                # Add triple to graph
                g.add((subject, predicate, Literal(str(value))))
            elif value is not None and attribute in pathlist and hasattr(self, 'sessionPath'):
                predicate = ld.match_uri(attribute)
                relpath=os.path.relpath(value,self.sessionPath)
                g.add((subject, predicate, Literal(relpath)))
        self.graph=g

    def get_path(self):
        """
        Get resource (full) path
        """
        allSessionFilePaths=ld.getListOfFiles(self.sessionPath) 
        for path in allSessionFilePaths:
            if self.name in path:
                self.path=path
                return True
        return False   
    
    

