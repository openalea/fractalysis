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
utils nodes
"""

__license__= "Cecill-C"
__revision__=" $Id: utils_nodes.py $ "



#from core.core import Node
#from openalea.core.interface import IFloat
#from openalea.core.interface import IStr
from openalea.core import *
import PlantGL as pgl
import openalea.fractalysis._pglcompute as pglc
import pylab as p

class boxMethod( Node ):
    """Box Method a.k.a counting intercepted voxel at each scale
    Input 0 : PlantGL scene
    Input 1 : final subdivision factor > 2
    Output 1 : array of voxels size
    Output 2 : array of intercepted voxels"""

    def __init__( self ):

        Node.__init__( self )

        #defines I/O
        self.add_input( name = 'scene', interface=None )
        self.add_input( name = 'finalSubFactor', interface=IInt, value=3 )
        self.add_output( name = 'scales', interface=None )
        self.add_output( name = 'interceptedVoxels', interface = None )

    def __call__( self, inputs= () ):
        res = pglc.computeGrids( self.get_input_by_key( 'scene' ), self.get_input_by_key( 'finalSubFactor' ) )
        
        sc=[]
        iv = []
        for r in res:
            sc.append( r[ 1 ] )
            iv.append( r[ 0 ] )
        scales =  p.log( 1./ p.array( sc ) )
        interVox = p.log( p.array( iv ) )
        print "scales :", scales
        print "interVox :", interVox

        return ( scales, interVox )


