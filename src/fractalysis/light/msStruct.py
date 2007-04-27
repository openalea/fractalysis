#from _light import *
import os
import openalea.plantgl.all as pgl
import skyTurtle as skt
import openalea.fractalysis.fractutils
fruti = openalea.fractalysis.fractutils
import cPickle
import csv
from PIL import Image
from time import sleep

#savedir = "/home/ddasilva/dev/fractalysis/Results/light"
#beam_file = "peachtree4_L.beams"
#sproj_file = "peachtree4_L.sproj"
#beam_file = "cantor.beams"
#sproj_file = "cantor.sproj"

def saveBeams(self,skt_idx, beams, pth=os.path.abspath(os.curdir)):
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name)
  savedir = os.path.join(pth, self.name)
  beam_file = self.name + "_skt_"+ str(skt_idx) + ".beams"
  dir = skt.getSkyTurtleDir(skt_idx)
  dir.normalize()
  param = {'dir':(dir.x, dir.y, dir.z)}
  result = {'beams':beams}
  res = fruti.ParamRes(param, result)
  if not os.path.isdir(savedir):
    os.mkdir(savedir) 
  file = os.path.join(savedir, beam_file)
  f = open(file, 'a')
  cPickle.dump(res, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()

def loadBeams(self, skt_idx, pth=os.path.abspath(os.curdir)):
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name)
  savedir = os.path.join(pth, self.name)
  beam_file = self.name + "_skt_"+ str(skt_idx) + ".beams"
  dir = skt.getSkyTurtleDir(skt_idx)
  dir.normalize()
  file = os.path.join(savedir, beam_file)
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

def saveSproj(self, skt_idx, sproj, pth=os.path.abspath(os.curdir)):
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name)
  savedir = os.path.join(pth, self.name)
  sproj_file = self.name + "_skt_"+ str(skt_idx) + ".sproj"
  dir = skt.getSkyTurtleDir(skt_idx)
  dir.normalize()
  param = {'dir':(dir.x, dir.y, dir.z)}
  result = {'sproj':sproj}
  res = fruti.ParamRes(param, result)
  if not os.path.isdir(savedir):
    os.mkdir(savedir) 
  file = os.path.join(savedir, sproj_file)
  f = open(file, 'a')
  cPickle.dump(res, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()

def loadSproj(self,skt_idx, pth=os.path.abspath(os.curdir)):
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name)
  savedir = os.path.join(pth, self.name)
  sproj_file = self.name + "_skt_"+ str(skt_idx) + ".sproj"
  dir = skt.getSkyTurtleDir(skt_idx)
  dir.normalize()
  file = os.path.join(savedir, sproj_file)
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

def makePict(self, skt_idx, distrib, matrix, width, height, pth=os.path.abspath(os.curdir)):
  dir = "img_skt_" + str(skt_idx)
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name, dir)
  savedir = os.path.join(pth, self.name, dir)
  if not os.path.isdir(savedir):
    os.mkdir(savedir) 
  dis=""
  for d in distrib:
    dis+=str(d)
  pic_file = dis +".jpg"
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

def prepareScene(self, scene, skt_idx, width, height, dist_factor=4):
  dir = skt.getSkyTurtleDir(skt_idx)
  pgl.Viewer.start()
  pgl.Viewer.display(scene)
  bbox=pgl.BoundingBox( scene )
  pgl.Viewer.animation( True )
  pgl.Viewer.grids.set(False,False,False,False)
  pgl.Viewer.camera.setOrthographic()
  pgl.Viewer.frameGL.setSize(width,height)
  d_factor = max(bbox.getXRange() , bbox.getYRange() , bbox.getZRange())
  pgl.Viewer.camera.lookAt(bbox.getCenter() + dir*(-dist_factor)*d_factor, bbox.getCenter())
  pgl.Viewer.display(scene)
  return dir

def checkFactor(self, factor):
  for i in range(1,47):
    self.prepareScene(self.genScaleScene(1), i, 300,300, factor)
    sleep(0.5)
  
#def computeProjections2(self, skt_idx, width=600, height=600):
#  dir = skt.getSkyTurtleDir(skt_idx)
#  dir.normalize()
#  total = []
#  for s in range(self.countScale()):
#    print "scale ",s+1
#    sc=pgl.Scene([ pgl.Shape(pgl.Translated(-pgl.BoundingBox(i.geometry).getCenter(),i.geometry),i.appearance,i.id) for i in self.genScaleScene(s+1)]) #center each shape of scene
#    pgl.Viewer.display(sc)
#    self.prepareScene(sc, skt_idx, width, height)
#    proj = pgl.Viewer.frameGL.getProjectionSizes(pgl.Viewer.getCurrentScene())
#    total += proj
#  return total

def computeDir(self, skt_idx, distrib=None, width=300, height=300, d_factor=4, pth=os.path.abspath(os.curdir)):
  if distrib== None:
    distrib=[['R','R','R','R'],['R','R','R','U'],['R','R','U','R'],['R','U','R','R'],['U','R','R','R'],['U','U','U','U'],['U','U','U','R'],['U','U','R','U'],['U','R','U','U'],['R','U','U','U']]

  dir = skt.getSkyTurtleDir(skt_idx)
  dir.normalize()
  az,el,wg = skt.getSkyTurtleAt(skt_idx)

  globScene = self.genScaleScene(1)
  for i in range(1,self.depth):
    globScene.add(self.genScaleScene(i+1))

  self.prepareScene(globScene, skt_idx, width, height, d_factor)
  #raw_input("Hit return when scene is completely visible in GL frame")
  
  b=self.loadBeams(skt_idx)
  if b != None:
    print "beams loaded..."
  else :
    print "computing beams..."
    b=pgl.Viewer.frameGL.castRays2(pgl.Viewer.getCurrentScene())
    self.saveBeams(skt_idx,b)
  self.beamsToNodes(dir, b)

  sproj=self.loadSproj(skt_idx)
  if sproj != None:
    print "projected surface loaded..."
    self.sprojToNodes(dir, sproj)
  else :
    print "computing projections..."
    sproj=self.computeProjections( dir )
    self.saveSproj(skt_idx, sproj)

  res=[]
  row=[] #line to write in csv file
  row.append(skt_idx)   #skyTurtle index
  row.append(str(az).replace('.',','))        #azimut
  row.append(str(el).replace('.',','))        #elevation
  row.append(dir)       #vector
  
  root_id = self.get1Scale(1)[0]
  s_classic = self.starClassic(root_id, dir)
  row.append(str(s_classic).replace('.',',')) #star with uniform leaves distribution in root hull
  for d in distrib:
    print "computing ",d,"..."
    matrix = self.probaImage(root_id, dir, d, width, height)
    self.makePict(skt_idx,d, matrix, width, height)
    s=self.star(root_id, dir, d)
    po = self.getNode(root_id).getPOmega(dir,d)
    res.append((d, s, po ))
    row.append(str(s).replace('.',','))
    row.append(str(po).replace('.',','))

  row.append(str(wg).replace('.',','))

  #writing in file
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name)
  savedir = os.path.join(pth, self.name)
  csv_file = self.name + ".csv"
  file = os.path.join(savedir, csv_file)
  writer = csv.writer(open(file, 'ab'), dialect='excel')
  writer.writerow(row)
  
  return res
