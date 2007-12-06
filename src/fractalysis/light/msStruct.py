#from _light import *
import os
import openalea.plantgl.all as pgl
#import skyTurtle as skt
import sunDome as sd
import openalea.fractalysis.fractutils
fruti = openalea.fractalysis.fractutils
import cPickle
import csv
from PIL import Image
from time import sleep
from math import radians, pi

#savedir = "/home/ddasilva/dev/fractalysis/Results/light"
#beam_file = "peachtree4_L.beams"
#sproj_file = "peachtree4_L.sproj"
#beam_file = "cantor.beams"
#sproj_file = "cantor.sproj"

def azel2vect(az, el):
  v = -pgl.Vector3(pgl.Vector3.Spherical( 1, radians( az ), radians( 90 - el ) ) )
  v.normalize()
  return v

#def saveBeams(self,skt_idx, beams, pth=os.path.abspath(os.curdir)):
def saveBeams(self,az, el, beams, pth=os.path.abspath(os.curdir)):
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name)
  savedir = os.path.join(pth, self.name)
  #beam_file = self.name + "_skt_"+ str(skt_idx) + ".beams"
  beam_file = self.name + "_az_"+ str(round(az,2)) + "_el_" + str(round(el,2)) + ".beams"
  #dir = skt.getSkyTurtleDir(skt_idx)
  #dir.normalize()
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

#def loadBeams(self, skt_idx, pth=os.path.abspath(os.curdir)):
def loadBeams(self, az, el, pth=os.path.abspath(os.curdir)):
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name)
  savedir = os.path.join(pth, self.name)
  #beam_file = self.name + "_skt_"+ str(skt_idx) + ".beams"
  beam_file = self.name + "_az_"+ str(round(az,2)) + "_el_" + str(round(el,2)) + ".beams"
  #dir = skt.getSkyTurtleDir(skt_idx)
  #dir.normalize()
  dir = azel2vect(az, el)
  file = os.path.join(savedir, beam_file)
  print "loading ", file
  if os.path.isfile( file ):
    f = open( file, 'r' )
    try:
      while( 1 ):
        res = cPickle.load( f )
        if res.testParamEq( "dir", ( dir.x,dir.y,dir.z ) ):
          beams = res.getResult( 'beams' )
          return beams
    except EOFError:
      f.close()
  else :
    print"file does not exist"
    return None

#def saveSproj(self, skt_idx, sproj, pth=os.path.abspath(os.curdir)):
def saveSproj(self, az, el, sproj, pth=os.path.abspath(os.curdir)):
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name)
  savedir = os.path.join(pth, self.name)
  #sproj_file = self.name + "_skt_"+ str(skt_idx) + ".sproj"
  sproj_file = self.name + "_az_"+ str(round(az,2)) + "_el_" + str(round(el,2)) + ".sproj"
  #dir = skt.getSkyTurtleDir(skt_idx)
  #dir.normalize()
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

#def loadSproj(self,skt_idx, pth=os.path.abspath(os.curdir)):
def loadSproj(self,az, el, pth=os.path.abspath(os.curdir)):
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name)
  savedir = os.path.join(pth, self.name)
  #sproj_file = self.name + "_skt_"+ str(skt_idx) + ".sproj"
  sproj_file = self.name + "_az_"+ str(round(az,2)) + "_el_" + str(round(el,2)) + ".sproj"
  #dir = skt.getSkyTurtleDir(skt_idx)
  #dir.normalize()
  dir = azel2vect(az, el)
  file = os.path.join(savedir, sproj_file)
  print "loading ", file
  if os.path.isfile( file ):
    f = open( file, 'r' )
    try:
      while( 1 ):
        res = cPickle.load( f )
        if res.testParamEq( "dir", ( dir.x,dir.y,dir.z ) ):
          sproj = res.getResult( 'sproj' )
          return sproj
    except EOFError:
      f.close()
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

#def prepareScene(scene, width, height, skt_idx=False, dist_factor=4):
def prepareScene(scene, width, height, az, el, dist_factor=4):
  #if( skt_idx):
  #  dir = skt.getSkyTurtleDir(skt_idx)
  if( az and el):
    dir = azel2vect(az, el)
  else :
    dir = pgl.Viewer.camera.getPosition()[1]
    dir.normalize()
  pgl.Viewer.start()
  pgl.Viewer.display(scene)
  bbox=pgl.BoundingBox( scene )
  pgl.Viewer.animation( True )
  pgl.Viewer.grids.set(False,False,False,False)
  pgl.Viewer.camera.setOrthographic()
  d_factor = max(bbox.getXRange() , bbox.getYRange() , bbox.getZRange())
  pgl.Viewer.camera.lookAt(bbox.getCenter() + dir*(-dist_factor)*d_factor, bbox.getCenter())
  pgl.Viewer.frameGL.setSize(width,height)
  #pgl.Viewer.display(scene)
  return dir


#def makePict(self, skt_idx, distrib, matrix, width, height, pth=os.path.abspath(os.curdir)):
def makePict(self, az, el, distrib, matrix, width, height, pth=os.path.abspath(os.curdir)):
  #dir = "img_skt_" + str(skt_idx)
  #dir = "img_az_" + str(round(az,2)) + "_el_" + str(round(el,2))
  dis=""
  for d in distrib:
    dis+=str(d)
  dir = "img_" + dis 
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name, dir)
  savedir = os.path.join(pth, self.name, dir)
  if not os.path.isdir(savedir):
    os.mkdir(savedir) 
  #pic_file = dis +".jpg"
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

#def computeDir(self, skt_idx, distrib=None, width=300, height=300, d_factor=4, pth=os.path.abspath(os.curdir)):
def computeDir(self, az=90, el=90, wg=False, distrib=None, skt_idx = False, width=300, height=300, d_factor=4, pth=os.path.abspath(os.curdir)):
  if distrib== None:
    distrib=[['R']*(self.depth - 1)]

  #dir = skt.getSkyTurtleDir(skt_idx)
  #dir.normalize()
  if(skt_idx) :
    az,el,wg = sd.getSkyTurtleAt(skt_idx)

  dir = azel2vect(az, el)

  globScene = self.genScaleScene(1)
  for i in range(1,self.depth):
    globScene.add(self.genScaleScene(i+1))

  #prepareScene(globScene, width, height, skt_idx=skt_idx, dist_factor=d_factor)
  prepareScene(globScene, width, height, az, el, dist_factor=d_factor)
  
  n = self.getNode(self.get1Scale(1)[0])
  if (n.getProjSurface(dir) == 0 ):
    #b=self.loadBeams(skt_idx, pth)
    b=self.loadBeams(az, el, pth)
    if b != None:
      print "beams loaded..."
    else :
      print "computing beams..."
      b=pgl.Viewer.frameGL.castRays2(pgl.Viewer.getCurrentScene())
      #self.saveBeams(skt_idx,b, pth)
      self.saveBeams(az, el,b, pth)
    self.beamsToNodes(dir, b)
  
    #sproj=self.loadSproj(skt_idx, pth)
    sproj=self.loadSproj(az, el, pth)
    if sproj != None:
      print "projected surface loaded..."
      self.sprojToNodes(dir, sproj)
    else :
      print "computing projections..."
      sproj=self.computeProjections( dir )
      #self.saveSproj(skt_idx, sproj, pth)
      self.saveSproj(az, el, sproj, pth)
  
  res=[]
  row=[] #line to write in csv file
  #row.append(skt_idx)   #skyTurtle index
  row.append(az)        #azimut
  row.append(el)        #elevation
  #row.append(dir)       #vector
  
  root_id = self.get1Scale(1)[0]
  s_classic = self.starClassic(root_id, dir)
  row.append(s_classic) #star with uniform leaves distribution in root hull
  res.append(('Beer', s_classic)) 
  for d in distrib:
    print "computing ",d,"..."
    matrix = self.probaImage(root_id, dir, d, width, height)
    #self.makePict(skt_idx,d, matrix, width, height, pth)
    self.makePict(az, el, d, matrix, width, height, pth)
    s=self.star(root_id, dir, d)
    po = self.getNode(root_id).getPOmega(dir,d)
    res.append((d, s, po ))
    row.append(s)
    row.append(po)

  if (wg):
    row.append(wg)

  #writing in file
  savedir = os.path.join(pth, self.name)
  csv_file = self.name + ".csv"
  file = os.path.join(savedir, csv_file)
  writer = csv.writer(open(file, 'ab'), dialect='excel')
  writer.writerow(row)
  
  return res

#####################extra functions not mandatory to light interception###############################

def checkFactor(self, width, height, factor):
  pix_width = 0
  for i in range(1,47):
    az, el, soc = sd.getSkyTurtleAt(i)
    #prepareScene(self.genScaleScene(1), 300,300, skt_idx = i, dist_factor=factor)
    prepareScene(self.genScaleScene(1), width, height, az, el, dist_factor=factor)
    pix_width += pgl.Viewer.frameGL.getProjectionSize()[2]
    sleep(0.3)
  return pix_width / 46.
  
#def directionalG(self, skt_idx, **kwds):
def directionalG(self, az, el, **kwds):
  #dir = skt.getSkyTurtleDir(skt_idx)
  #dir.normalize()
  dir = azel2vect(az, el)
  pth = kwds.get( 'pth', os.path.abspath(os.curdir) )
  width = kwds.get('width', 300)
  height = kwds.get('height', 300)
  scale = kwds.get('scale', self.depth)

  #sproj=self.loadSproj(skt_idx, pth)
  sproj=self.loadSproj(az, el, pth)
  if sproj != None:
    print "projected surface loaded..."
    self.sprojToNodes(dir, sproj)
  else :
    print "computing projections..."
    sproj=self.computeProjections( dir )
    #self.saveSproj(skt_idx, sproj, pth)
    self.saveSproj(az, el, sproj, pth)
  
  nodelist = self.get1Scale(scale)
  ratio = 0
  for idx in nodelist:
    n = self.getNode(idx)
    ratio += n.getProjSurface(dir) / n.surface 

  return ratio / len(nodelist)
  

def getPEA(self, **kwds):
  width = kwds.get('width', 300)
  height = kwds.get('height', 300)
  d_factor = kwds.get('d_factor', 4)
  pth = kwds.get('pth', os.path.abspath(os.curdir))
  root_id = self.get1Scale(1)[0]
  #skyT = kwds.get('skyT', False)
  az = kwds.get('az', 0)
  el = kwds.get('el', 90)
  integrated = kwds.get('integrated', True)
  PEA = []
  if (integrated):
    globPEA = 0
    for s in range(1,47):
      #az, el, soc = skt.getSkyTurtleAt(s)
      az, el, soc = sd.getSkyTurtleAt(s)
      #dir = skt.getSkyTurtleDir(s)
      #dir.normalize()
      dir = azel2vect(az, el)
      #prepareScene(self.genScaleScene(1), width, height, skt_idx = s, dist_factor=d_factor)
      prepareScene(self.genScaleScene(1), width, height, az, el, dist_factor=d_factor)
      sproj = pgl.Viewer.frameGL.getProjectionSize()[0]
      PEA.append(sproj)
      globPEA += sproj*soc
    PEA.append(globPEA)
  else :
    #az, el, soc = skt.getSkyTurtleAt(skyT)
    #dir = skt.getSkyTurtleDir(skyT)
    #dir.normalize()
    dir = azel2vect(az, el)
    #prepareScene(self.genScaleScene(1), width, height, skt_idx = skyT, dist_factor=d_factor)
    prepareScene(self.genScaleScene(1), width, height, az, el, dist_factor=d_factor)
    sproj = pgl.Viewer.frameGL.getProjectionSize()[0]
    print "sproj", sproj, "soc", soc
    PEA.append(sproj*soc)
  return PEA

def vgStar(self, **kwds):
  width = kwds.get('width', 300)
  height = kwds.get('height', 300)
  d_factor = kwds.get('d_factor', 4)
  pth = kwds.get('pth', os.path.abspath(os.curdir))
  pos = kwds.get('pos', sd.skyTurtle() )
  root_id = self.get1Scale(1)[0]
  tla = self.totalLA(root_id)
  rstar = []
  #cstar = []
  #for s in range(1,47):
  for p in pos:
    #dir = skt.getSkyTurtleDir(s)
    #dir.normalize()
    dir = azel2vect(p[0], p[1])
    #prepareScene(self.genScaleScene(self.depth), width, height, skt_idx = s, dist_factor=d_factor)
    prepareScene(self.genScaleScene(self.depth), width, height, az, el, dist_factor=d_factor)
    sproj = pgl.Viewer.frameGL.getProjectionSize()[0]
    real_star = sproj / tla
    rstar.append(real_star)
    #writing result to file
    #az,el,wg = skt.getSkyTurtleAt(s)
    row=[] #line to write in csv file
    row.append(s)   #skyTurtle index
    #row.append(str(round(az,2)).replace('.',','))        #azimut
    #row.append(str(round(el,2)).replace('.',','))        #elevation
    row.append(az)
    row.append(el)
    #row.append(str(real_star).replace('.',',')) #star with uniform leaves distribution in root hull
    row.append(real_star)
    #row.append(str(wg).replace('.',','))
    savedir = os.path.join(pth, self.name)
    csv_file = self.name + "_vgstar.csv"
    file = os.path.join(savedir, csv_file)
    writer = csv.writer(open(file, 'ab'), dialect='excel')
    writer.writerow(row)

  #starReal = 0
  #starUnif = 0
  #for i,w in enumerate(skt.weights) :
    #starReal+= w*rstar[i]
    #starUnif+= w*cstar[i]

  #return starReal#, starUnif


