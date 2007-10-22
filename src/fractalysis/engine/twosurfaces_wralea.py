# -*- python -*-
#
#       OpenAlea.Fractalysis : OpenAlea fractal analysis library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Boudon Frederic <frederic.boudon@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Wralea for Fractalysis.TwoSurfaces
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
               'authors' : 'Boudon F.',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'fractalysis.twosurfaces nodes.',
               }


    package = Package("fractalysis.twosurfaces", metainfo)

###### begin nodes definitions #############

    nf = Factory( name="TwoSurfaces",
                  description="Computes two surfaces on a multiscale scenes",
                  category="Fractal Analysis",
                  nodemodule="twosurfaces",
                  nodeclass="TwoSurfaces",
                  inputs=(dict(name="leaves", interface=None,),
                          dict(name="macrorep", interface=ISequence),
                          ),
                  outputs=(dict(name="macrosurfaces", interface = ISequence),
                           dict(name="microsurfaces", interface = ISequence),),
                  )

    package.add_factory( nf )


###### end nodes definitions ###############

    pkgmanager.add_package(package)