import sunDome as sd
from _light import ssFromDict
import openalea.plantgl.all as pgl

from math import radians, pi



def directStar(scene, lat=43.36, long=3.52, jj=221, start=7, stop=19, stp=30, dsun = 1, dGMT = 0, w=150, h=150, dfact=8):
  """
  Compute STAR from the sun course directions given the following parameters:
  
  :Parameters:
    - `scene` : scene for which the STAR is to be computed
    - `lat`   : latitude of location, default = 43.36
    - `long`  : longitude of location, default = 3.52
    - `jj`    : Julian day, default = 221
    - `start` : first hour to be considered, default = 7
    - `stop`  : last hour to be considered, default = 19
    - `step`  : time step in minutes between 2 sun positions, default = 30
    - `dsun`  : correction factor or something needs to be documented, default = 1
    - `dGMT`  : factor related to time zone needs to be documented, default=0
    - `w`     : width of viewer frame, default =150
    - `h`     : height of viewer frame, default=150
    - `dfact` : distance factor for camera positioning i.e. 2.5 for 600x600 or 8 for 150x150, default=8

  :Types:
    - `scene` : plantGL scene
    - `lat`   : float
    - `long`  : float
    - `jj`    : int
    - `start` : float
    - `stop`  : float
    - `step`  : int
    - `dsun`  : int 
    - `dGMT`  : int
    - `w`     : int
    - `h`     : int
    - `dfact` : int

  :returns: STAR value from SOC coefficient
  :returntype: float
  """
  direct = sd.getDirectLight( latitude=lat , longitude=long, jourJul=jj, startH=start, stopH=stop, step=stp, decalSun = dsun, decalGMT = dGMT)
  return  myStar(scene, directions = direct,  w=w, h=h, dfact=dfact)

def diffuStar(scene, w=150, h=150, dfact=8):
  """
  Compute STAR for the diffuse light dirrectons based on Den Dulk's turtle sky and given the following parameters:
  
  :Parameters:
    - `scene` : scene for which the STAR is to be computed
    - `w`     : width of viewer frame, default =150
    - `h`     : height of viewer frame, default=150
    - `dfact` : distance factor for camera positioning i.e. 2.5 for 600x600 or 8 for 150x150, default=8

  :Types:
    - `scene` : plantGL scene
    - `w`     : int
    - `h`     : int
    - `dfact` : int

  :returns: STAR value from SOC coefficient
  :returntype: float
  """
 
  return myStar(scene, w=w, h=h, dfact=dfact)

def myStar(scene, directions = sd.skyTurtle(), w=150, h=150, dfact=8, wr=False):
  tab=[{1:[sh.getId() for sh in scene]}]
  mss=ssFromDict('myTree', scene, tab, "Cvx Hull")
  star = mss.vgStar(pos = directions, width=w, height=h, d_factor=dfact, write=wr)
  return star

def decomposedSTAR(scene, directions = sd.skyTurtle(), w=150, h=150, dfact=8, wr=False):
  tab=[{1:[sh.getId() for sh in scene]}]
  mss=ssFromDict('myTree', scene, tab, "Cvx Hull")
  iPEA, TLA = mss.vgStar(pos = directions, width=w, height=h, d_factor=dfact, write=wr, details=True)
  return iPEA/TLA, iPEA, TLA


  ###### myStar from scratch ##################
  #pgl.Viewer.display(scene)
  #redrawPol = pgl.Viewer.redrawPolicy
  #pgl.Viewer.redrawPolicy = False
  #pgl.Viewer.frameGL.maximize(True)
  #pgl.Viewer.widgetGeometry.setSize(600, 600)
  #pgl.Viewer.frameGL.setSize(600,600)
  #
  #pgl.Viewer.camera.setOrthographic()
  #pgl.Viewer.grids.set(False,False,False,False)
  #bbox=pgl.BoundingBox( scene )
  #d_factor = max(bbox.getXRange() , bbox.getYRange() , bbox.getZRange())
 
  ##scc=pgu.centerScene( scene )
  ##pgu.viewScene(scc)
  #tab=[{1:[sh.getId() for sh in scene]}]
  #mss=ssFromDict('myTree', scene, tab, "Cvx Hull")
  #root = mss.get1Scale(1)[0]
  #totalLA = mss.totalLA(root)
  #sumSilhouette = 0
  #for d in  directions:
  #  az,el,wg = d
  #  if( az != None and el != None):
  #    dir = azel2vect(az, el)
  #  else :
  #    dir = -pgl.Viewer.camera.getPosition()[1]

  #  pgl.Viewer.camera.lookAt(bbox.getCenter() + dir*(-2.5)*d_factor, bbox.getCenter()) #2.5 is for a 600x600 GLframe

  #  sproj, pixnum, pixsize = pgl.Viewer.frameGL.getProjectionSize()
  #  sumSilhouette += sproj * wg

  #return sumSilhouette / totalLA


def diffuseInterception(scene):
  return  directionalInterception(scene, directions = sd.skyTurtle())

def directInterception(scene, lat=43.36, long=3.52, jj=221, start=7, stop=19, stp=30, dsun = 1, dGMT = 0):
  direct = sd.getDirectLight( latitude=lat , longitude=long, jourJul=jj, startH=start, stopH=stop, step=stp, decalSun = dsun, decalGMT = dGMT)
  return  directionalInterception(scene, directions = direct)

def totalInterception(scene, lat=43.36, long=3.52, jj=221, start=7, stop=19, stp=30, dsun = 1, dGMT = 0):
  diffu = sd.skyTurtle()
  direct =  sd.getDirectLight( latitude=lat , longitude=long, jourJul=jj, startH=start, stopH=stop, step=stp, decalSun = dsun, decalGMT = dGMT)
  all = direct + diffu
  return directionalInterception(scene, directions = all)


# converter for azimuth elevation 
# az,el are expected in degrees, in the North-clocwise convention
# In the scene, positive rotations are counter-clockwise
#north is the angle (degrees, positive counter_clockwise) between X+ and North
def azel2vect(az, el, north=0):
  azimuth = radians(north - az)
  zenith = radians(90 - el)
  v = -pgl.Vector3(pgl.Vector3.Spherical( 1., azimuth, zenith ) )
  v.normalize()
  return v



def directionalInterception(scene, directions, north = 0, horizontal = False):
  
  pgl.Viewer.display(scene)
  redrawPol = pgl.Viewer.redrawPolicy
  pgl.Viewer.redrawPolicy = False
  pgl.Viewer.frameGL.maximize(True)
  pgl.Viewer.widgetGeometry.setSize(600, 600)
  pgl.Viewer.frameGL.setSize(600,600)
  
  cam_pos,cam_targ,cam_up = pgl.Viewer.camera.getPosition()
  pgl.Viewer.camera.setOrthographic()
  pgl.Viewer.grids.set(False,False,False,False)
  bbox=pgl.BoundingBox( scene )
  d_factor = max(bbox.getXRange() , bbox.getYRange() , bbox.getZRange())
  shapeLight = {}

  for az, el, wg in directions:
    if( az != None and el != None):
        dir = azel2vect(az, el, north)
        if horizontal :
            wg /= sin(radians(el))

    else :
      dir = -pgl.Viewer.camera.getPosition()[1]
      assert not horizontal

    pgl.Viewer.camera.lookAt(bbox.getCenter() + dir*(-2.5)*d_factor, bbox.getCenter()) #2.5 is for a 600x600 GLframe

    values = pgl.Viewer.frameGL.getProjectionPerShape()
    if not values is None:
      nbpixpershape, pixsize = values
      pixsize = pixsize*pixsize
      for key,val in nbpixpershape:
        if shapeLight.has_key(key):
          shapeLight[key] += val*pixsize*wg
        else:
          shapeLight[key] = val*pixsize*wg
  #valist = [shapeLight[key] for key in shapeLight.keys() ]
  #print "Min value : ", min(valist)
  #print "Max value : ", max(valist)
  pgl.Viewer.camera.lookAt(cam_pos, cam_targ ) 
  pgl.Viewer.redrawPolicy = redrawPol

  
  return shapeLight


def sceneIrradiance(scene, directions, north = 0, horizontal = False, scene_unit = 'm'):
    """
    Compute the irradiance received by all the shapes of a given scene.
   :Parameters:
    - `scene` : scene for which the irradiance has to be computed
    - `directions` : list of tuple composed of the an azimuth, an elevation and an irradiance (in J.s-1.m-2)
    - `north` : the angle between the north direction of the azimuths (in degrees)
    - `horizontal` : specify if the irradiance use an horizontal convention (True) or a normal direction (False)
    - `scene_unit` : specify the units in which the scene is built. Convert then all the result in m.

    :returns: the area of the shapes of the scene in m2 and the irradiance in J.s-1.m-2
    :returntype: pandas.DataFrame
    """

    units = {'mm': 0.001, 'cm': 0.01, 'dm': 0.1, 'm': 1, 'dam': 10, 'hm': 100,
             'km': 1000}

    conv_unit = units[scene_unit]
    conv_unit2 = conv_unit**2


    res = directionalInterception(scene, directions, north, horizontal)
    res = { sid : conv_unit2 * value for sid, value in res.iteritems() }

    surfaces = dict([(sid, conv_unit2*sum([surface(sh.geometry) for sh in shapes])) for sid, shapes in scene.todict().iteritems()])


    irradiance = { sid : value / surfaces[sid] for sid, value in res.iteritems() }

    import pandas
    return pandas.DataFrame( {'area' : surfaces, 'irradiance' : irradiance} )
