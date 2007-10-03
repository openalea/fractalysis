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
Wralea for Fractalysis.Library 
"""

__license__= "Cecill-C"
__revision__=" $Id$ "



from openalea.core import *
from scipy import arange

myrange = [str(i) for i in arange(0.05, 1, 0.05)]
#myrange = arange(0.05, 1, 0.05)

def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """


    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'DDS',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'utils nodes.',
               }


    package = Package("fractalysis.utils", metainfo)

###### begin nodes definitions #############

    nf = Factory( name="Trees from file",
                  description="Generates a set of trees from a dendrometric description file",
                  category="Modelling",
                  nodemodule="genStands",
                  nodeclass="treesFromFile",
                  inputs = (dict(name="CSV file", interface=IFileStr,),
                            ),
                  outputs = (dict(name="treeList", interface = None),
                            ),
                  )

    package.add_factory( nf )

    nf = Factory( name="Trees to Scene",
                  description="Generates a stand scene from a set of Trees",
                  category="Modelling",
                  nodemodule="genStands",
                  nodeclass="makeScene",
                  inputs = ( dict(name="Trees", interface=None,),
                             #dict(name="Midcrown limit", interface=IFloat, value=0.5),
                             dict(name="Midcrown limit", interface=IEnumStr(myrange),),
                             dict(name="Include wood", interface=IBool,),
                             dict(name="Random positions", interface=IBool,),
                           ),
                  outputs = ( dict(name="stand", interface = None),
                            ),
                  )

    package.add_factory( nf )


###### end nodes definitions ###############

    pkgmanager.add_package(package)


