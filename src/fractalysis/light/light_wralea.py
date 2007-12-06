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

def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """


    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'DDS',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'fractalysis.light nodes.',
               }


    package = Package("fractalysis.light", metainfo)

###### begin nodes definitions #############

    nf = Factory( name="create MSS",
                  description="Generates a multi scale structure",
                  category="Light",
                  nodemodule="light_nodes",
                  nodeclass="create_MSS",
                  inputs=(dict(name="name", interface=IStr,),
                          dict(name="scene", interface=None,),
                          dict(name="scale table", interface=ISequence,),
                          ),
                  outputs=(dict(name="MSS", interface = None,),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="generatePix",
                  description="Generates directional shadow picture",
                  category="Light",
                  nodemodule="light_nodes",
                  nodeclass="generate_pix",
                  inputs=(dict(name="MSS", interface=None,),
                          dict(name="Light direction", interface=ISequence,),
                          dict(name="Distribution", interface=ISequence,),
                          dict(name="Image size", interface=ISequence,),
                          dict(name="Save path", interface=IDirStr,),
                          dict(name="Dist factor", interface=IFloat(min=1), value=4, hide=True),
                          ),
                  outputs=(dict(name="Image", interface = None,),
                          ),
                  )

    package.add_factory( nf )


    nf = Factory( name="Light direction",
                  description="Defines the direction of incident light",
                  category="Light",
                  nodemodule="light_nodes",
                  nodeclass="light_direction",
                  inputs= ( dict( name = "Azimuth", interface=IFloat, value = 10),
                            dict( name = "Elevation", interface=IFloat, value = 52.62),
                          ),
                  outputs=( dict( name = "Light direction", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

###### end nodes definitions ###############

    pkgmanager.add_package(package)


