from pathlib import Path as P
import cv2 as cv,numpy as np,subprocess as sp,hashlib,json,os
from jsonschema import validate
cv.setNumThreads(2);J=lambda p:json.loads(P(p).read_text());H=lambda p:hashlib.sha256(P(p).read_bytes()).hexdigest();plan=J('montage/partition.json');j=J('livraison/job.json');validate(j,J('schemas/render-job.json'));fps=plan['fps'];W,Y=plan['dimensions'];shots=J('render/demo/rushs.json');assert len({c['sha256'] for c in j['captures']})==4;assert all([x['scene']==y['id'] and x['duree_s']*fps==y['fin_exclue']-y['debut'] for x,y in zip([dict(scene='S'+str(s['scene']),duree_s=s['duree_s']) for s in J('capture-guide/ecrans.json')['ecrans'][::3]],plan['scenes'])]);out=P('livraison/COMMERCE-T3-Regarde-comment-ca-marche.mp4');enc=sp.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{Y}','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=sp.PIPE);samples=[];scenes=[]
def crop(img,w,h,cx,cy,z=1):
 ih,iw=img.shape[:2];cw=min(iw,ih*w/h)/z;ch=cw*h/w;l=int(np.clip(iw*cx-cw/2,0,iw-cw));t=int(np.clip(ih*cy-ch/2,0,ih-ch));return cv.resize(img[t:t+round(ch),l:l+round(cw)],(w,h),interpolation=cv.INTER_LINEAR)
xx=np.abs(np.linspace(-1,1,W))[None,:];yy=np.linspace(0,1,Y)[:,None];mask=(.63*np.maximum(np.clip((xx-.61)/.39,0,1),np.clip((.16-yy)/.16,0,1)))[:,:,None].astype('float32');maps={}
for k,(shot,sc,entry) in enumerate(zip(shots,plan['scenes'],j['captures'])):
 sid=sc['id'];p=P('work')/(sid+'.mp4');assert entry['scene']==sid==shot['scene'] and H(p)==entry['sha256']==shot['sha256'];cap=cv.VideoCapture(str(p));hz=cap.get(5);first,last=sc['debut'],sc['fin_exclue'];start=int(shot['entree_s']*hz);cap.set(1,start);cursor=start-1;ret=None
 for i in range(first,last):
  pos=start+int((i-first)*hz/fps)
  while cursor<pos:
   ok,ret=cap.read();assert ok;cursor+=1
  if k==1:
   f=np.zeros((Y,W,3),np.uint8)
   for h,(x,y,z) in enumerate([(.50,.48,1),(.54,.18,1.52),(.58,.51,1.35),(.49,.69,1.3)]):
    r=h//2*(Y//2);c=h%2*(W//2);f[r:r+Y//2-2,c:c+W//2-2]=crop(ret,W//2-2,Y//2-2,x,y,z)
  else:
   f=crop(ret,W,Y,shot['centre_x'],.5)
   if k in (0,3):
    rule=plan['raccords'][k];col=rule['couleurs'][sum(t<=i for t in rule['images'])-1];color=np.array([int(col[q:q+2],16) for q in (5,3,1)],dtype='float32');f=(f*(1-mask)+color*mask).astype('uint8')
  txt=cv.imread('work/titres/'+str(i)+'.png',cv.IMREAD_UNCHANGED);a=txt[:,:,3:4].astype('float32')/255;top=535 if k==1 else 845;roi=f[top:top+200];roi[:]=roi*(1-a)+txt[:,:,:3]*a;enc.stdin.write(f.tobytes());
  if i in (18,120,250,390,510,626,698,877):samples.append(cv.resize(f,(144,256)))
 cap.release();scenes.append(dict(scene=sid,source=entry['sha256'],debut=first,fin_exclue=last,premiere_image_source=start,derniere_image_source=cursor))
enc.stdin.close();assert enc.wait()==0;cv.imwrite('livraison/Planche.jpg',np.hstack(samples));probe=J if False else json.loads(sp.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(out)]));v,=probe['streams'];assert v['codec_type']=='video' and v['codec_name']=='h264' and v['nb_read_frames']=='900' and v['r_frame_rate']=='30/1' and (v['width'],v['height'])==(720,1280) and float(probe['format']['duration'])==30;assert (not j['reponses'].get('prix')) and not J('livraison/titres.json')['prix'];report=dict(template_id=j['template_id'],commit=os.environ['GITHUB_SHA'],fps=30,frames=900,duree_s=30,dimensions=[W,Y],codec='h264',audio_streams=0,sha256=H(out),scenes=scenes,ecrans=j['ecrans'],prix_facultatif_non_affiche=True,source_des_textes='réponses du job navigateur + libellés du gabarit',empreinte_partition=H('montage/partition.json'),grille_quatre_vues_meme_prise=True);P('livraison/controle.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
