# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): David Da SILVA <david.da_silva@cirad.fr>
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
__revision__=" $Id: utils_nodes.py $ "

from openalea.core import *
import openalea.plantgl.all as pgl
import openalea.fractalysis.engine as engine
import pylab as p

class BCM( Node ):
    """Box Method a.k.a counting intercepted voxel at each scale
    Input 0 : PlantGL scene
    Input 1 : final subdivision factor > 2
    Output 1 : array of voxels size
    Output 2 : array of intercepted voxels"""

    def __init__( self, inputs, outputs ):

        Node.__init__( self, inputs, outputs )

    def __call__( self, inputs ):
        scene = pgl.Scene(self.get_input( 'scene' ))
        res = engine.computeGrids( scene , self.get_input( 'stopFactor' ) )
        
        sc=[]
        iv = []
        for r in res:
            sc.append( r[ 1 ] )
            iv.append( r[ 0 ] )
        scales =  p.log( 1./ p.array( sc ) )
        interVox = p.log( p.array( iv ) )

        return ( scales, interVox )


