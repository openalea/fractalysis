#from _light import *
import os
import openalea.plantgl.all as pgl
import sunDome as sd
import openalea.fractalysis.fractutils
fruti = openalea.fractalysis.fractutils
import cPickle
import csv
from PIL import Image
from time import sleep, time
from math import radians, pi
from scipy import array, sum
from openalea.catalog.color.py_color import rgb_color_map

def azel2vect(az, el):
  v = -pgl.Vector3(pgl.Vector3.Spherical( 1, radians( az ), radians( 90 - el ) ) )
  v.normalize()
  return v

def saveBeams(self,az, el, beams, pth=os.path.abspath(os.curdir)):
  savedir = os.path.join(pth, self.name)
  beam_file = self.name + "_az_"+ str(round(az,2)) + "_el_" + str(round(el,2)) + ".beams"
  dir = azel2vect(az, el)
  param = {'dir':(dir.x, dir.y, dir.z)}
  result = {'beams':beams}
  res = fruti.ParamRes(param, result)
  if not os.path.isdir(savedir):
    os.mkdir(savedir) 
  file = os.path.join(savedir, beam_file)
  f = open(file, 'a')
  cPickle.dump(res, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()
  print "beams saved"

def loadBeams(self, az, el, pth=os.path.abspath(os.curdir)):
  savedir = os.path.join(pth, self.name)
  beam_file = self.name + "_az_"+ str(round(az,2)) + "_el_" + str(round(el,2)) + ".beams"
  dir = azel2vect(az, el)
  file = os.path.join(savedir, beam_file)
  print "loading ", file
  if os.path.isfile( file ):
    f = open( file, 'r' )
    try:
      res = cPickle.load( f )
      beams = res.getResult( 'beams' )
      return beams
    except EOFError:
      f.close()
      return None
  else :
    print"file does not exist"
    return None

def saveSproj(self, az, el, sproj, pth=os.path.abspath(os.curdir)):
  savedir = os.path.join(pth, self.name)
  sproj_file = self.name + "_az_"+ str(round(az,2)) + "_el_" + str(round(el,2)) + ".sproj"
  dir = azel2vect(az, el)
  param = {'dir':(dir.x, dir.y, dir.z)}
  result = {'sproj':sproj}
  res = fruti.ParamRes(param, result)
  if not os.path.isdir(savedir):
    os.mkdir(savedir) 
  file = os.path.join(savedir, sproj_file)
  f = open(file, 'a')
  cPickle.dump(res, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()
  print "sproj saved"

def loadSproj(self,az, el, pth=os.path.abspath(os.curdir)):
  savedir = os.path.join(pth, self.name)
  sproj_file = self.name + "_az_"+ str(round(az,2)) + "_el_" + str(round(el,2)) + ".sproj"
  dir = azel2vect(az, el)
  file = os.path.join(savedir, sproj_file)
  print "loading ", file
  if os.path.isfile( file ):
    f = open( file, 'r' )
    try:
      res = cPickle.load( f )
      sproj = res.getResult( 'sproj' )
      return sproj
    except EOFError:
      f.close()
      return None
  else :
    print"file does not exist"
    return None


def removeScale(self, sc):
  assert sc > 0 and sc < self.depth, "sc not in range"
  for idx in self.get1Scale( sc - 1 ):
    self.getNode( idx ).components = []
  for idx in self.get1Scale( sc ) :
    n = self.getNode( idx )
    n.scale = -1
    cplx = n.cplx
    for cp in n.components :
      self.sonOf( cp, cplx )
  for s in range( sc + 1, self.depth + 1):
    for i in self.get1Scale( s ) :
      self.getNode( i ).scale = s-1
  self.countScale() 

def prepareScene(scene, width=150, height=150, az=None, el=None, dist_factor=8):
  if( az != None and el != None):
    dir = azel2vect(az, el)
  else :
    dir = -pgl.Viewer.camera.getPosition()[1]
    dir.normalize()
  pgl.Viewer.start()
  pgl.Viewer.animation( True )
  pgl.Viewer.display(scene)
  bbox=pgl.BoundingBox( scene )
  pgl.Viewer.grids.set(False,False,False,False)
  pgl.Viewer.camera.setOrthographic()
  d_factor = max(bbox.getXRange() , bbox.getYRange() , bbox.getZRange())
  pgl.Viewer.camera.lookAt(bbox.getCenter() + dir*(-dist_factor)*d_factor, bbox.getCenter())
  pgl.Viewer.frameGL.setSize(width,height)
  pgl.Viewer.frameGL.setSize(width,height)
  return dir


def makePict(self, az, el, distrib, matrix, width, height, pth=os.path.abspath(os.curdir)):
  dis=""
  for d in distrib:
    dis+=str(d)
  dir = "img_" + dis 
  savedir = os.path.join(pth, self.name, dir)
  if not os.path.isdir(savedir):
    os.mkdir(savedir) 
  pic_file = "az_" + str(round(az,2)) + "_el_" + str(round(el,2)) + ".jpg"
  file = os.path.join(savedir, pic_file)
  img = Image.new('L', (width, height))
  for x in range(height):
    for y in range(width):
      ndg = 255-255*matrix[x][y]
      try :
        img.putpixel((x,y), ndg) #cause picture are 1/4 clockwise rotated
      except OverflowError:
        print "too big value : ", matrix[x][y]
        img.putpixel((x,y), 0) #cause picture are 1/4 clockwise rotated
  out = img.rotate(90)
  out.save(file, "JPEG")
  return out

def computeDir(self, az=90, el=90, wg=False, distrib=None, skt_idx = False, width=150, height=150, d_factor=8, pth=os.path.abspath(os.curdir)):
  if distrib== None:
    distrib=[['A']*(self.depth - 1)]

  if(skt_idx) :
    az,el,wg = sd.getSkyTurtleAt(skt_idx)

  dir = azel2vect(az, el)

  n = self.getNode(self.get1Scale(1)[0])
  if (n.getProjSurface(dir) == 0 ):
    b=self.loadBeams(az, el, pth)
    if b != None:
      print "beams loaded..."
      self.beamsToNodes(dir, b)
    else :
      print "computing beams..."
      b=self.computeBeams(dir, width, height, d_factor)
      self.saveBeams(az, el,b, pth)
  
    sproj=self.loadSproj(az, el, pth)
    if sproj != None:
      print "projected surface loaded..."
      self.sprojToNodes(dir, sproj)
    else :
      print "computing projections..."
      sproj=self.computeProjections( dir )
      self.saveSproj(az, el, sproj, pth)
  
  res={}
  row=[] #line to write in csv file
  #row.append(skt_idx)   #skyTurtle index
  row.append(az)        #azimut
  row.append(el)        #elevation
  #row.append(dir)       #vector
  
  root_id = self.get1Scale(1)[0]
  s_classic = self.starClassic(root_id, dir)
  row.append(s_classic) #star with uniform leaves distribution in root hull
  res['Star_turbid'] =  s_classic
  for d in distrib:
    print "computing ",d,"..."
    matrix = self.probaImage(root_id, dir, d, width, height)
    img = self.makePict(az, el, d, matrix, width, height, pth)
    s=self.star(root_id, dir, d)
    po = self.getNode(root_id).getPOmega(dir,d)
    res['Star_'+str(d)] = s
    res['Pix_'+str(d)] = img
    row.append(s)
    #row.append(po)

  if (wg):
    row.append(wg)

  #writing in file
  savedir = os.path.join(pth, self.name)
  csv_file = self.name + ".csv"
  file = os.path.join(savedir, csv_file)
  writer = csv.writer(open(file, 'ab'), dialect='excel')
  writer.writerow(row)
  
  return res

def recieved_light(self, scale, az=90, el=90, wg=1, mode="Multiscale", width=150, height=150, d_factor=8, pth=os.path.abspath(os.curdir)):
  v = azel2vect(az,el)

  if mode == "Multiscale":
    distrib=[['R']*(self.depth - 1)]
    if(self.getNode(self.get1Scale(1)[0]).getPOmega(v,distrib[0]) == -1):
      self.computeDir(az=az, el=el, wg=wg, distrib=distrib, width=width, height=height, d_factor=d_factor, pth=pth)
    beams = self.loadBeams(az, el, pth)
    sc_distrib = ['R']*(self.depth - scale)
    res = self.availight(scale, v, beams, sc_distrib)

    scene = self.genScaleScene(scale)
    vals = [res[id] for id in res.keys()]
    m = min(vals)
    M = max(vals)
    for id in res.keys():
      sh = scene.find(id)
      r,g,b = rgb_color_map(value=(M-res[id]), minval=m, maxval=M, hue1=0, hue2=140)[0]
      sh.appearance = fruti.color(r/3, g/3, b/3, diffu=3)
    return res, scene
    
  elif mode == "Real":
    print "atual mode"
    return 1,1
  elif mode == "Turbid":
    print "turbid mode"
    return 2,2

def compute4Errors(self, peach = False, az=90, el=90, wg=False, skt_idx = False, width=150, height=150, d_factor=8, pth=os.path.abspath(os.curdir)):

  if(skt_idx) :
    az,el,wg = sd.getSkyTurtleAt(skt_idx)

  dir = azel2vect(az, el)

  results={}

  root_id = self.get1Scale(1)[0]
  n = self.getNode(root_id)

  if (n.getProjSurface(dir) == 0 ):
    b=self.loadBeams(az, el, pth)
    if b != None:
      print "beams loaded..."
      self.beamsToNodes(dir, b)
    else :
      print "computing beams..."
      b=self.computeBeams(dir, width, height, d_factor)
      print "now saving..."
      self.saveBeams(az, el,b, pth)
  
    sproj=self.loadSproj(az, el, pth)
    if sproj != None:
      print "projected surface loaded..."
      self.sprojToNodes(dir, sproj)
    else :
      print "computing projections..."
      sproj=self.computeProjections( dir )
      self.saveSproj(az, el, sproj, pth)

  if(peach):
    distrib = [['R','R','R','R'], ['R','R','A','A'], ['R','R','R','A']]
  else:
    distrib = [['R','R','R'], ['R','R','A']]

  results['az'] = az
  results['el'] = el
  results['wg'] = wg

  res = {}
 
  pea = n.getProjSurface(dir)
  tla = self.totalLA(root_id)
  res['pea'] = pea
  res['tla'] = tla

  sc = self.genNodeScene(root_id)
  sc.remove(n.shape)
  prepareScene(sc, 150, 150, az, el)
  pla = pgl.Viewer.frameGL.getProjectionSize()[0]
  essai = 0
  while pla == 0 and essai < 500:
    prepareScene(sc, 150, 150, 155, 90)
    prepareScene(sc, 150, 150, az, el)
    print "getprojectionsize : ", pgl.Viewer.frameGL.getProjectionSize()
    pla = pgl.Viewer.frameGL.getProjectionSize()[0]
    essai += 1
  if essai < 500 :
    res['pla'] = pla
  else : 
    res['pla'] = 0.001

  star_turbid = self.starClassic(root_id, dir)    
  res['turbid'] = star_turbid

  for d in distrib:
    print "computing ",d,"..."
    s=self.star(root_id, dir, d)    
    po = n.getPOmega(dir,d)
    res[tuple(d)] = (s, po)
 
  results[root_id] = res
  #root is done now doing the same for all components of all scales except last one
  for scale in range(2, self.depth):
    compo = self.get1Scale(scale)
    
    print "new scale distrib : "
    for d in distrib:
      d.pop(0)
      print d

    for id in compo:
      res = {}
      n = self.getNode(id)
   
      pea = n.getProjSurface(dir)
      tla = self.totalLA(id)
      res['pea'] = pea
      res['tla'] = tla

      sc = self.genNodeScene(id)
      sc.remove(n.shape)
      prepareScene(sc, 150, 150, az, el)
      pla = pgl.Viewer.frameGL.getProjectionSize()[0]
      essai = 0
      while pla == 0 and essai < 500:
        prepareScene(sc, 150, 150, 155, 90)
        prepareScene(sc, 150, 150, az, el)
        #print "getprojectionsize : ", pgl.Viewer.frameGL.getProjectionSize()
        pla = pgl.Viewer.frameGL.getProjectionSize()[0]
        essai += 1
      if essai < 500 :
        res['pla'] = pla
      else :
        print "pla problem for component : ", id
        res['pla'] = 0.001

      star_turbid = self.starClassic(id, dir)    
      res['turbid'] = star_turbid
      for d in distrib:
        s = self.star(id, dir, d)    
        po = n.getPOmega(dir,d)
        res[tuple(d)] = (s, po)
   
      results[id] = res

  savedir = os.path.join(pth, self.name)
  sproj_file = self.name + "_az_"+ str(round(az,2)) + "_el_" + str(round(el,2)) + ".err"
  if not os.path.isdir(savedir):
    os.mkdir(savedir) 
  file = os.path.join(savedir, sproj_file)
  f = open(file, 'w')
  cPickle.dump(results, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()

  return results


#####################extra functions not mandatory to light interception###############################

def checkFactor(self, width, height, factor, pause=0.1):
  pix_width = 0
  for i in range(1,47):
    az, el, soc = sd.getSkyTurtleAt(i)
    prepareScene(self.genScaleScene(1), width, height, az, el, dist_factor=factor)
    pix_width += pgl.Viewer.frameGL.getProjectionSize()[2]
    sleep(pause)
  return pix_width / 46.
  
def directionalG(self, az, el, **kwds):
  dir = azel2vect(az, el)
  pth = kwds.get( 'pth', os.path.abspath(os.curdir) )
  width = kwds.get('width', 150)
  height = kwds.get('height', 150)
  scale = kwds.get('scale', self.depth)

  sproj=self.loadSproj(az, el, pth)
  if sproj != None:
    print "projected surface loaded..."
    self.sprojToNodes(dir, sproj)
  else :
    print "computing projections..."
    sproj=self.computeProjections( dir )
    self.saveSproj(az, el, sproj, pth)
  
  nodelist = self.get1Scale(scale)
  ratio = 0
  for idx in nodelist:
    n = self.getNode(idx)
    ratio += n.getProjSurface(dir) / n.surface 

  return ratio / len(nodelist)
  

def getPEA(self, **kwds):
  width = kwds.get('width', 150)
  height = kwds.get('height', 150)
  d_factor = kwds.get('d_factor', 8)
  pth = kwds.get('pth', os.path.abspath(os.curdir))
  root_id = self.get1Scale(1)[0]
  az = kwds.get('az', 0)
  el = kwds.get('el', 90)
  integrated = kwds.get('integrated', True)
  PEA = []
  if (integrated):
    globPEA = 0
    for s in range(1,47):
      az, el, soc = sd.getSkyTurtleAt(s)
      dir = azel2vect(az, el)
      prepareScene(self.genScaleScene(1), width, height, az, el, dist_factor=d_factor)
      sproj = pgl.Viewer.frameGL.getProjectionSize()[0]
      PEA.append(sproj)
      globPEA += sproj*soc
    PEA.append(globPEA)
  else :
    dir = azel2vect(az, el)
    prepareScene(self.genScaleScene(1), width, height, az, el, dist_factor=d_factor)
    sproj = pgl.Viewer.frameGL.getProjectionSize()[0]
    print "sproj", sproj, "soc", soc
    PEA.append(sproj*soc)
  return PEA

def vgStar(self, **kwds):
  start = time()
  width = kwds.get('width', 150)
  height = kwds.get('height', 150)
  d_factor = kwds.get('d_factor', 8)
  pth = kwds.get('pth', os.path.abspath(os.curdir))
  pos = kwds.get('pos', sd.skyTurtle() )
  write = kwds.get('write', True )
  root_id = self.get1Scale(1)[0]
  tla = self.totalLA(root_id)
  rstar = []
  soc = []
  for s,p in enumerate(pos):
    az = p[0]
    el = p[1]
    wg = p[2]
    dir = azel2vect(az, el)
    prepareScene(self.genScaleScene(self.depth), width, height, az, el, dist_factor=d_factor)
    sproj = pgl.Viewer.frameGL.getProjectionSize()[0]
    real_star = sproj / tla
    rstar.append(real_star)
    soc.append(wg)
    #writing result to file
    if write :
      row=[] #line to write in csv file
      row.append(s+1)
      row.append(az)
      row.append(el)
      row.append(wg)
      row.append(real_star)
      savedir = os.path.join(pth, self.name)
      if not os.path.isdir(savedir):
        os.mkdir(savedir) 
      csv_file = self.name + "_vgstar.csv"
      file = os.path.join(savedir, csv_file)
      writer = csv.writer(open(file, 'ab'), dialect='excel')
      writer.writerow(row)
  stop = time()
  print "total computation time : ", stop-start, " s."
  return sum(array(rstar) * array(soc))

