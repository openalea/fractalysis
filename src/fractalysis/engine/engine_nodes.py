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


__doc__="""
fractalysis.engine nodes
"""

__license__= "Cecill-C"
__revision__=" $Id: engine_nodes.py $ "

from copy import deepcopy
from scipy import log, array
from openalea.core import *
import openalea.plantgl.all as pgl
#import openalea.fractalysis.engine as engine
from openalea.fractalysis.engine import computeGrids
from openalea.fractalysis.engine.lac_engine import MatrixLac
from openalea.fractalysis.fractutils.pgl_utils import surfPerTriangle, gridIndex, color, scene2grid, toPglScene

class BCM( Node ):
    """Box Method a.k.a counting intercepted voxel at each scale
    Input 0 : PlantGL scene
    Input 1 : final subdivision factor > 2
    Output 1 : array of voxels size
    Output 2 : array of intercepted voxels"""

    def __init__( self, inputs, outputs ):

        Node.__init__( self, inputs, outputs )

    def __call__( self, inputs ):
        #scene = pgl.Scene(self.get_input( 'scene' ))
        scene = self.get_input( 'scene' ) 
        res = computeGrids( scene , self.get_input( 'stopFactor' ) )
        
        sc=[]
        iv = []
        for r in res:
            sc.append( r[ 1 ] )
            iv.append( r[ 0 ] )
        #scales =  log( 1./ array( sc ) )
        #interVox = log( array( iv ) )
        scales =   1./ array( sc ) 
        interVox =  array( iv ) 
        return ( scales, interVox )

class Voxels(object):

    def __init__(self, size, centers, density=None):

        self.size = size
        self.centers = centers
        self.density = density

    def __repr__(self):
        
        return "Voxels size : " + str(self.size) + "\n Voxels centers : " + str(self.centers) + "\n Voxels density : " + str(self.density)


def voxelize(scene, gridSize, density=True ):
  """generate the scene resulting of grid discretization"""
  #scene = pgl.Scene(sceneFile)
  bbox = pgl.BoundingBox(scene)
  epsilon = pgl.Vector3( 0.01, 0.01, 0.01 )
  origin = bbox.lowerLeftCorner - epsilon
  step = ( bbox.getSize() + epsilon )*2 / ( gridSize )
  origin_center = origin + step/2.
  
  tgl_list = surfPerTriangle( scene )

  grid = {}
  for tgl in tgl_list:
    pos = gridIndex( tgl[ 0 ] - origin, step )
    assert( pos[ 0 ] < gridSize and pos[ 1 ] < gridSize and pos[ 2 ] < gridSize )

    if grid.has_key(  pos  ):
      grid[  pos  ] += tgl[ 1 ]
    else:
      grid[  pos  ] = tgl[ 1 ]

  kize = grid.keys()
  kize.sort()
  pts=[]
  mass=[]
  for k in kize:
    pts.append(  list( k )  )
    mass.append( grid[ k ] )
    
  massort = deepcopy( mass )
  massort.sort()
  qlist=[25, 50, 75]
  quants = [massort[int(len(massort)*q/100.0)] for q in qlist]
  
  voxSize = step/2.
  vox = pgl.Box( voxSize )
  vox.setName( 'voxel' )
  
  mat1 = color( 47,255,0, trans=True , name='c_green')
  mat2 = color( 255,255,0, trans=True , name='c_yellow')
  mat3 = color( 255,170,0, trans=True , name='c_orange')
  mat4 = color( 255,0,0, trans=True , name='c_red')

  #sc = pgl.Scene()
  ctrs = []
  for i in range( len( pts ) ):
    pt = pts[ i ]
    vect = pgl.Vector3( origin_center.x + ( pt[ 0 ] * step.x ) , origin_center.y + ( pt[ 1 ] * step.y ) ,origin_center.z + ( pt[ 2 ] * step.z ) )
    ctrs.append(vect)
    geometry = pgl.Translated( vect, vox )
    if( density ):
      if ( mass[ i ] < quants[ 0 ] ) :
        sh = pgl.Shape( geometry, mat1, i )
      elif ( mass[ i ] < quants[ 1 ] ) :
        sh = pgl.Shape( geometry, mat2, i )
      elif ( mass[ i ] < quants[ 2 ] ) :
        sh = pgl.Shape( geometry, mat3, i )
      else :
        sh = pgl.Shape( geometry, mat4, i )
    else:
      sh = pgl.Shape( geometry, mat1, i )
    scene.add( sh )
  
  vxls = Voxels( voxSize, ctrs, mass ) 

  #return (vxls, scene)
  return ( voxSize, ctrs, mass, scene ) 


def lactrix_fromScene( scene, file_name, gridSize, spath, density):
  """
  Generate a `MatrixLac` instance from a PlantGL scene.

  :Parameters:
    - `file` : name of geom/bgeom scene file, without extension
    - `gridSize` : subdivision factor of the bonuding box defining the grid step
    - `density` : when True each non-empty voxel is associated with a proper value (e.g. leaf area density inside each voxel)

  :Types:
    - `file` : string
    - `gridSize` : int
    - `density` : boolean
  
  :returns: `MatrixLac` instance generated from the scene
  :returntype: `MatrixLac`

  """
  ( pts, m, s ) = scene2grid( scene, gridSize )
  if ( not density ):
    print "Density not taken into account..."
    mat=MatrixLac( name=file_name, points=pts, size=gridSize, vox_size = s, mass=None, spath = spath )
    visu = toPglScene( mat.points) 
  else:
    print "Considering Density..."
    mat=MatrixLac( name=file_name, points=pts, size=gridSize, vox_size = s, mass=m, spath = spath )
    visu = toPglScene( mat.points, m ) 
  return mat, visu 

class lacunarity( Node ):
  """
  Compute the lacunarity of a n-dimensional matrix
  """

  lac_func =  { "Centered" : "_ctrdlac",
                "Allain & Cloitre" : "_lacac",
              }

  def __init__(self):

    Node.__init__(self)
    funs = self.lac_func.keys()
    funs.sort()
    self.add_input( name = "Matrix", interface=None,)
    self.add_input( name = "Type", interface = IEnumStr(funs), value=funs[-1])
    self.add_input( name = "Start", interface = IInt(min = 0) )
    self.add_input( name = "Stop", interface = IInt(min = 0) )
    self.add_output( name = "Lacunarity", interface = ISequence)
    self.add_output( name = "Box sizes", interface = ISequence)

  def __call__(self, inputs):
    func_name = self.get_input("Type")
    f = self.lac_func[func_name]
    self.set_caption(func_name)
    mat = self.get_input("Matrix")
    lac, boxes = mat.lacunarity(  radius_start = self.get_input("Start"),
                                  radius_stop = self.get_input("Stop"),
                                  lac_type = getattr(mat,f),
                                )
    box_size = [pgl.norm(b) for b in boxes]

    return lac, box_size
