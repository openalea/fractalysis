# -*- python -*-
#
#       OpenAlea.Fractalysis : OpenAlea Fractalysis module
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
#from openalea.core.interface import IFileStr
from openalea.core import *
import pgl_utils as pgu

class loadScene( Node ):
    """Load geom or bgeom scene
    Input 0 : File to load
    Output 0 : PlantGL scene"""

    def __init__( self ):

       Node.__init__( self )

       #defines I/O
       self.add_input( name = 'file', interface = IFileStr )
       self.add_output( name = 'scene', interface = None )

    def __call__( self, inputs=() ):
        return ( pgu.pgl.Scene( self.get_input_by_key( 'file' ) ), )

class viewScene( Node ):
    """Scene visualization using PlantGL's viewer
    Input 0 : geom scene"""

    def __init__( self ):

       Node.__init__( self )

       #defines I/O
       self.add_input( name = 'scene', interface = None )

    def __call__( self, inputs=() ):
        pgu.viewScene( self.get_input_by_key( 'scene' ) )
