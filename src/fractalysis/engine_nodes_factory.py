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
Factory for engine_nodes simplify the wralea file 
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "


from openalea.core.core import Factory


def define_factory(package):
    """ Define factories for arithmetics nodes """

    nf = Factory( name= "BCM", 
                      description= "Box Counting Method", 
                      category = "Analysis", 
                      nodemodule = "engine_nodes",
                      nodeclass = "boxMethod",
                      widgetmodule = None,
                      widgetclass = None, 
                      #parameters = [ 'finalSubFactor' ]
                      )

    package.add_factory( nf )


