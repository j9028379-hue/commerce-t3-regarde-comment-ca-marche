from pathlib import Path as P
import cv2 as cv,numpy as np,subprocess as sp,hashlib,json,os
from jsonschema import validate


cv.setNumThreads(2);J=lambda p:json.loads(P(p).read_text());H=lambda p:hashlib.sha256(P(p).read_bytes()).hexdigest();plan=J('montage/partition.json');j=J('livraison/job.json');validate(j,J('schemas/render-job.json'));fps=plan['fps'];W,Y=plan['dimensions'];shots=j['captures'];assert len({c['sha256'] for c in j['captures']})==4;assert all([x['scene']==y['id'] and x['duree_s']*fps==y['fin_exclue']-y['debut'] for x,y in zip([dict(scene='S'+str(s['scene']),duree_s=s['duree_s']) for s in J('capture-guide/ecrans.json')['ecrans'][::3]],plan['scenes'])]);out=P('livraison/COMMERCE-T3-Regarde-comment-ca-marche.mp4');enc=sp.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{Y}','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p','-metadata','comment=Images : LED Noodle Lantern, Ruiz Brothers / Adafruit, https://youtu.be/9Mak8Uz3F8c (CC BY). Extraits remontés, recadrés et titrés. Exemple fictif Boutique Élégance. Variation automatique après allumage.', '-movflags','+faststart',str(out)],stdin=sp.PIPE);samples=[];scenes=[]
def crop(img,w,h,cx,cy,z=1):
 ih,iw=img.shape[:2];cw=min(iw,ih*w/h)/z;ch=cw*h/w;l=int(np.clip(iw*cx-cw/2,0,iw-cw));t=int(np.clip(ih*cy-ch/2,0,ih-ch));return cv.resize(img[t:t+round(ch),l:l+round(cw)],(w,h),interpolation=cv.INTER_LINEAR)
liaisons=J('work/liaisons.json');assert plan['etalonnage']['mode']=='source_native' and sum(bool(v) for v in liaisons)==sum(v['duree'] for v in plan['liaisons']);prev=None
for k,(shot,sc,entry) in enumerate(zip(shots,plan['scenes'],j['captures'])):
 sid=sc['id'];p=P('work')/(sid+'.mp4');assert entry['scene']==sid==shot['scene'] and H(p)==entry['sha256']==shot['sha256'];cap=cv.VideoCapture(str(p));hz=cap.get(5);first,last=sc['debut'],sc['fin_exclue'];start=0;cap.set(1,start);cursor=-1;ret=None
 for i in range(first,last):
  pos=start+int((i-first)*hz/fps)
  while cursor<pos:
   ok,ret=cap.read();assert ok;cursor+=1
  if k==1:
   f=np.zeros((Y,W,3),np.uint8)
   rule=plan['raccords'][1];d=rule['trait_px']//2;order=[e['ordre'] for e in rule['coupes_cases'] if e['image']<=i][-1]
   for h,idx in enumerate(order):
    x,y,z=rule['cadrages'][idx];r=h//2*(Y//2+d);c=h%2*(W//2+d);hh,ww=Y//2-d,W//2-d;f[r:r+hh,c:c+ww]=crop(ret,ww,hh,x,y,z)
  else:
   f=crop(ret,W,Y,.5,.5)
  if i==last-1:prev=f.copy()
  if liaisons[i]:
   assert prev is not None;mask=np.zeros((Y,W),np.uint8)
   for poly in liaisons[i]['polys']:
    pts=np.int32(np.round(np.array(poly)*[W,Y]));
    if cv.contourArea(pts)>0:cv.fillConvexPoly(mask,pts,255,lineType=cv.LINE_AA)
   f=np.where((mask>127)[:,:,None],f,prev)
  txt=cv.imread('work/titres/'+str(i)+'.png',cv.IMREAD_UNCHANGED);a=txt[:,:,3:4].astype('float32')/255;top=plan['texte']['bande_export']['haut'];roi=f[top:top+txt.shape[0]];roi[:]=roi*(1-a)+txt[:,:,:3]*a;
  if i in (776,899):
   y,x=np.nonzero(a[:,:,0]>.50);assert len(y)>0 and y.max()+top<Y*.38 and y.min()+top>75 and y.max()-y.min()>=85 and x.max()-x.min()>350;cv.imwrite('livraison/'+('Boutique' if i==776 else 'Contact')+'.jpg',f)
  enc.stdin.write(f.tobytes());
  if i in (201,202,203,204):cv.imwrite('livraison/Onde-'+str(i)+'.jpg',f)
  if i in (18,120,203,390,510,626,698,877):samples.append(cv.resize(f,(144,256)))
 cap.release();scenes.append(dict(scene=sid,source=entry['sha256'],debut=first,fin_exclue=last,premiere_image_source=start,derniere_image_source=cursor))
enc.stdin.close();assert enc.wait()==0;cv.imwrite('livraison/Planche.jpg',np.hstack(samples));probe=json.loads(sp.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(out)]));v,=probe['streams'];assert v['codec_type']=='video' and v['codec_name']=='h264' and v['nb_read_frames']=='900' and v['r_frame_rate']=='30/1' and (v['width'],v['height'])==(720,1280) and float(probe['format']['duration'])==30;assert J('livraison/titres.json')['prix']==j['reponses'].get('prix','');report=dict(template_id=j['template_id'],commit=os.environ['GITHUB_SHA'],fps=30,frames=900,duree_s=30,dimensions=[W,Y],codec='h264',audio_streams=0,sha256=H(out),scenes=scenes,ecrans=j['ecrans'],prix_affiche=bool(j['reponses'].get('prix')),source_des_textes='liaison_champs du contrat appliquée au job navigateur ; aucun texte commercial fixe',teintes_ajoutees=False,transitions=plan['liaisons'],zone_contact='tiers supérieur',empreinte_partition=H('montage/partition.json'),grille_quatre_vues_meme_prise=True);P('livraison/controle.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
