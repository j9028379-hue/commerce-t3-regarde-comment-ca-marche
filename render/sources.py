from pathlib import Path as P
import json,subprocess as sp,hashlib
for row in json.loads(P('render/demo/rushs.json').read_text()):
 p=P('work')/(row['scene']+'.mp4');p.parent.mkdir(exist_ok=True);sp.run(['curl','-LfsS','--retry','3','--max-time','180',row['url'],'-o',p],check=True);assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
