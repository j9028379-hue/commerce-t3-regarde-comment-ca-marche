"""Vérifie le contrat de la démo sur les titres et sur des images décodées du MP4."""
import cv2,json,hashlib
from pathlib import Path as P
import numpy as np
J=lambda p:json.loads(P(p).read_text());job=J('livraison/job.json');plan=J('montage/partition.json');v=J('livraison/titres.json');rep=job['reponses'];assert rep=={q['cle']:q['exemple'] for q in J('form/questions.json')['champs']};caps=job['captures'];assert len(caps)==4 and len(set(c['sha256'] for c in caps))==4 and job['ecrans']==list(range(1,13));cap=cv2.VideoCapture('livraison/COMMERCE-T3-Regarde-comment-ca-marche.mp4');checks={};text=plan['texte'];
for wnd in text['fenetres']:
 k=wnd['champ'];actual=v[k];keys=text['liaison_champs'][k];assert actual==('WhatsApp\n' if k=='contact' else '')+'\n'.join(rep.get(q,'') for q in keys);f=wnd['fin_exclue']-2;cap.set(1,f);ok,img=cap.read();assert ok;overlay=cv2.imread(f'work/titres/{f}.png',-1);cible=np.array(list(bytes.fromhex(text['couleur'][1:]))[::-1],dtype=int);mask=(overlay[:,:,3]>245)&(np.max(abs(overlay[:,:,:3].astype(int)-cible),axis=2)<6);top=text['bande_export']['haut'];pixels=img[top:top+overlay.shape[0]][mask];assert len(pixels)>300 and (np.max(abs(pixels.astype(int)-cible),axis=1)<32).mean()>.85 and np.median(pixels[:,2].astype(int)-pixels[:,0])>=6;checks[k]=dict(champs=keys,valeur=actual,image_decodee=f,pixels_lettres_opaques=int(len(pixels)));assert set(keys)<=set(rep)
assert {q for c in checks.values() for q in c['champs']}==set(rep);P('livraison/preuve-champs.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False));cap.release()
