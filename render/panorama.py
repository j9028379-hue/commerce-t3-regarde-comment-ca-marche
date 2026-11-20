import cv2 as cv,numpy as np

def panorama(path):
 c=cv.VideoCapture(str(path));last=None;tiles=[];offset=np.zeros(2);step=24;cursor=-1;orb=cv.SIFT_create(1600);bf=cv.BFMatcher()
 while True:
  ok=False
  for _ in range(step if last else 1):ok=c.grab()
  if not ok:break
  ok,fr=c.retrieve();fr=cv.resize(fr,(960,540));gray=cv.cvtColor(fr,cv.COLOR_BGR2GRAY);kp,d=orb.detectAndCompute(gray,None)
  if last:
   mk,md=last;ms=[m for m,n in bf.knnMatch(d,md,k=2) if m.distance<.69*n.distance];dx=np.asarray([np.subtract(mk[v.trainIdx].pt,kp[v.queryIdx].pt) for v in ms]);offset+=np.median(dx,axis=0)
  last=kp,d;tiles.append((fr,offset.copy()))
 c.release();coords=np.int32(np.round([v for _,v in tiles]));coords-=coords.min(axis=0);w,h=coords.max(axis=0)+[960,540];canvas=np.zeros((h,w,3),np.uint8);filled=np.zeros((h,w),bool)
 for (tile,_),(x,y) in zip(tiles,coords):
  seen=filled[y:y+540,x:x+960];area=canvas[y:y+540,x:x+960];area[~seen]=tile[~seen];seen[:]=True
 return canvas
