import cv2 as cv,numpy as np
# La chrominance change, pas la luminance : aucun voile opaque sur le sujet.
def grade(img,hexcolor,k,look):
 hsv=cv.cvtColor(img,cv.COLOR_BGR2HSV);h,s,v=cv.split(hsv);lo,hi=look['teintes_jaunes_opencv'];atten=np.minimum(np.clip((h.astype(float)-lo+3)/3,0,1),np.clip((hi+3-h.astype(float))/3,0,1));s=(s*(1-(1-look['saturation_jaune'])*atten)).astype('uint8');neutral=cv.cvtColor(cv.merge([h,s,v]),cv.COLOR_HSV2BGR);lab=cv.cvtColor(neutral,cv.COLOR_BGR2Lab);color=np.uint8([[[int(hexcolor[z:z+2],16) for z in (5,3,1)]]]);t=cv.cvtColor(color,cv.COLOR_BGR2Lab)[0,0];height,width=h.shape;cx,cy,rx,ry=look['contours_proteges_par_scene'][k];y,x=np.ogrid[0:height,0:width];dist=((x/width-cx)/rx)**2+((y/height-cy)/ry)**2;weight=(look['intensite_decor_grille'] if k==1 else look['intensite_decor'])*(1-look['protection_produit']*np.clip((1.22-dist)/.50,0,1));
 for i in (1,2):lab[:,:,i]=(lab[:,:,i]*(1-weight)+float(t[i])*weight).astype('uint8')
 return cv.cvtColor(lab,cv.COLOR_Lab2BGR)
