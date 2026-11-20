"""Télécharge le film autorisé sur le runner, extrait uniquement les plans tournés."""
import hashlib, json, subprocess as sp
from pathlib import Path
m=json.loads(Path('render/demo/plans-filmes.json').read_text()); w=Path('work'); w.mkdir(exist_ok=True); p=w/'source-lanterne.mp4'
sp.run(['curl','-fsSL','--retry','3','--max-time','100',m['source'],'-o',str(p)],check=True)
assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256']
for s in m['plans']:
    # Reframing optique seulement, aucune teinte, pas de dessin. Laisser le temps de voir la prise USB.
    vf=f"crop=trunc(ih*9/16/2)*2:ih:iw*{s['cx']}-ow/2:0,scale=720:1280,setsar=1,setpts=(PTS-STARTPTS)*{s['sortie']/s['extrait']},fps=30,tpad=stop_mode=clone:stop_duration=0.2"
    sp.run(['ffmpeg','-loglevel','error','-y','-ss',str(s['debut']),'-t',str(s['extrait']),'-i',str(p),'-map','0:v:0','-an','-vf',vf,'-frames:v',str(s['sortie']*30),'-c:v','libx264','-crf','16','-preset','veryfast','-pix_fmt','yuv420p',str(w/(s['id']+'.mp4'))],check=True)
Path('livraison').mkdir(exist_ok=True); Path('livraison/plans-filmes.json').write_text(json.dumps(m,indent=2,ensure_ascii=False))
