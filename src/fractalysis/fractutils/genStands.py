#! /usr/bin/env python
# -*- python -*-
#
#       OpenAlea.Fractalysis : OpenAlea fractal analysis library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


"""
:Authors:
  - Da SILVA David
:Organization: Virtual Plants
:Contact: david.da_silva:cirad.fr
:Version: 1.0
:Date: August 2007
:requires:
  - plantgl
  - random
  - math
  - pgl_utils

Module for generating stands of tree according to mesure.

"""

__docformat__ = "restructuredtext en"


from random import uniform
import openalea.plantgl.all as pgl
from openalea.fractalysis.fractutils.pgl_utils import sphere, arrow, color, createSwung

houppier_material = pgl.Material("houppier_mat",pgl.Color3(20,100,60))
trunk_material = pgl.Material("trunk_material",pgl.Color3(50,28,6),2)

from math import pi
class Tree:

  def __init__(self, id, nid, essence, pos_x, pos_y, radius, haut, base_houp):
    """
    
    Constructor of `Tree`

    :Parameters:
      - `id` : identifier of the tree
      - `numid` : numerical identifier of the tree
      - `essence` : the tree species
      - `pos_x` : the tree x position in the stand
      - `pos_y` : the tree y position in the stand
      - `radius` : the radius of the trunk
      - `haut` : the tree height
      - `base_houp` : the height of the begining of the tree canopy

    :Types:
      - `id` : string
      - `numid` : int
      - `essence` : string
      - `pos_x` : float
      - `pos_y` : float
      - `radius` : float
      - `haut` : float
      - `base_houp` : float

    :return: instance of `Tree`
    :returntype: `Tree`

    :Note: all mesures are in cm

    """

    self.id=id
    self.numid=nid
    self.essence = essence
    self.x = pos_x
    self.y = pos_y
    self.radius = radius
    self.height = haut
    self.base_houp = base_houp
    self.houppier = []

  def addDirectionHouppier(self, dist, az):
    """
    Helper function : add a characteristic direction to the canopy

    :Parameters:
      - `dist` : orthogonal projection of the length from trunk to canopy border
      - `az` : azimuthal angle for the direction

    :Types:
      - `dist` : float
      - `az` : float

    """
    self.houppier.append((dist,az))
  
  def meanHoup(self):
    som = 0.0
    nbHoup = len(self.houppier)
    for i in range(nbHoup):
      som+=self.houppier[i][1]
    return som/nbHoup
  
  def __repr__(self):
    return "Arbre : "+ str(self.id) +"    "+ str(self.essence) +'\n'+"Position : ["+str(self.x)+","+str(self.y)+"]    rayon : "+ str(self.radius)+ "    hauteur : "+ str(self.height)+'\n'+ "Base houppier : "+str(self.base_houp)+ "    Carac (distance,azimut) : "+ str(self.houppier)
  
  def geometry(self, midCrown = 0.5, rdm_x=None, rdm_y=None):
    self.houppier.sort(cmp = lambda x,y : cmp(x[1],y[1]))
    mc = float(midCrown)
    radii = list(self.houppier)
    ht = self.height-self.base_houp
    if (rdm_x == None and rdm_y == None):
      h = pgl.Translated(pgl.Vector3(self.x,self.y,self.base_houp),createSwung(ht*mc,ht,radii))
      tr = pgl.Translated(pgl.Vector3(self.x,self.y,0),pgl.Cylinder(self.radius,self.base_houp+ht*0.2))
    else:
      rx=uniform(min(rdm_x), max(rdm_x))
      ry=uniform(min(rdm_y), max(rdm_y))
      h = pgl.Translated(pgl.Vector3(rx,ry,self.base_houp),createSwung(ht*mc,ht,radii))
      tr = pgl.Translated(pgl.Vector3(rx,ry,0),pgl.Cylinder(self.radius,self.base_houp+ht*0.2))

    s_h = pgl.Shape(h,houppier_material,self.numid+1)
    s_tr = pgl.Shape(tr,trunk_material,self.numid+100000)
    return s_h,s_tr
  
  def mesures(self, id=0):
    gr=[]
    gr.append(sphere(self.x, self.y, 0, radius=20, color=color(0,0,255),slice=10,stack=10,id=id))
    for d in self.houppier:
      if d[0]>0:
        gr.append(arrow(self.x, self.y, 0, d[0], az=d[1],radius=5,id=id))
    return gr

def treesFromFile( file, c_id=1, c_ess=2, c_posx=6, c_posy=7, c_radius=8, c_height=9, c_crownbase=10, c_crownDir_start=12 ):
  """
  Parse a csv file containing stand cartography and trees dendrometric informations to generate trees. The first 2 lines are reserved to column descriptions and notes. Mandatory column are described in parameters.

  :Note: starting from `c_crownDir_start` the parser take values 2 by 2 as length and azimutal direction for specific crown radii until there is no more value in the line.

  :Parameters:
    - `c_id` : column containing tree id
    - `c_ess` : column containing tree essence
    - `c_posx` : column containing tree x position
    - `c_posy` : column containing tree y position
    - `c_radius` : column containing tree trunk perimeter at 1.3m height
    - `c_height` : column containing tree height
    - `c_crownbase` : column containing tree canopy base height
    - `c_crownDir_start` : column starting the list of tree canopy characteristic radii

  :Types:
    - `c_id` : int
    - `c_ess` : int
    - `c_posx` : int
    - `c_posy` : int
    - `c_radius` : int
    - `c_height` : int
    - `c_crownbase` : int
    - `c_crownDir_start` : int

  :return: a list of `Tree` instances
  :returntype: `Tree` list

  """

  treeList=[]
  f=open(file, 'r')
  cont = f.readlines()
  f.close()
  for i in range(2, len(cont)):
    line = cont[i].split(',')
    t = Tree(id=line[c_id], nid=i-1, essence=line[c_ess], pos_x=float(line[c_posx]), pos_y=float(line[c_posy]), radius=float(line[c_radius])/(2*pi), haut=float(line[c_height])*100, base_houp=float(line[c_crownbase])*100)
    for v in range(c_crownDir_start, len(line),2):
      try:
        t.addDirectionHouppier(int(line[v]), 90-((int(line[v+1])+200)%400 )*0.9)
      except ValueError:
        break
    treeList.append(t)
  return (treeList,)

   
def makeScene( trees, midCr = 0.5, wood=True, random=False):
  #treeList = treesFromFile(file)
  treeList = trees
  scene=pgl.Scene()
  x = [t.x for t in treeList]
  y = [t.y for t in treeList]
  for i in range(len(treeList)):
    t=treeList[i]
    if random:
      h,tr = t.geometry(midCrown = midCr, rdm_x=(min(x),max(x)), rdm_y=(min(y),max(y)))
    else:
      h,tr = t.geometry(midCrown = midCr)
    scene.add(h)
    if(wood):
      scene.add(tr)
  return (scene,)

def viewMesures( file):
  treeList = treesFromFile(file)
  scene = pgl.Scene()
  for i in range(len(treeList)):
    t=treeList[i]
    mes = t.mesures(i)
    for sh in mes:
      scene.add(sh)
  pgl.Viewer.display(scene)


#treeList=makeScene('/home/ddasilva/dev/fractalysis/PlantDB/stands/placette1.csv')
#treeList=makeScene('/home/ddasilva/dev/fractalysis/PlantDB/stands/placette3.csv')
