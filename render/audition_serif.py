"""Reprendre le son du comparatif validé sans modifier ses paquets AAC."""
import subprocess as sp,json
from pathlib import Path as P
D=P('livraison').resolve();v=D/'COMMERCE-T3-Regarde-comment-ca-marche.mp4';a=P('render/demo/audition/4-mix.m4a');out=D/'Boutique-Elegance-4-mix-Serif.mp4';lst=P('work/4-films.txt');lst.write_text((f"file '{v}'\n" )*4);credit=P('render/demo/audition/CREDITS.txt').read_text()+' Images : LED Noodle Lantern — Ruiz Brothers / Adafruit, CC BY, https://youtu.be/9Mak8Uz3F8c ; extraits montés et titrés.'
sp.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(lst),'-i',str(a),'-map','0:v:0','-map','1:a:0','-c','copy','-metadata','comment='+credit,'-movflags','+faststart',str(out)],check=True)
def h(p):return sp.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
probe=json.loads(sp.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(out)]));assert int(probe['streams'][0]['nb_frames'])==3600 and abs(float(probe['streams'][1]['duration'])-120)<.2 and h(a)==h(out);print('3600 images, AAC identique :',h(out));
