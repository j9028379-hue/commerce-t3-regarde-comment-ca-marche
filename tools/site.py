from pathlib import Path as P
import json
j=lambda p:json.loads(P(p).read_text());q=j('form/questions.json');s=j('capture-guide/ecrans.json')['ecrans'];p=j('montage/partition.json');assert len(q['champs'])==6 and [a['cle'] for a in q['champs'] if not a['obligatoire']]==['prix'] and q['champs'][3]['cle']=='demonstration';assert [a['numero'] for a in s]==list(range(1,13));assert [(a['scene'],a['etat'],a['duree_s']) for a in s]==[(i,c,d) for i,d in enumerate([6,8,7,9],1) for c in 'ABC'];assert p['images']==p['fps']*30 and [(a['debut'],a['fin_exclue']) for a in p['scenes']]==[(0,180),(180,420),(420,630),(630,900)];P('docs/data.js').write_text('const T3='+json.dumps(dict(form=q,ecrans=s,plan=p,carte=j("catalogue/catalogue.json")["entries"][0]),ensure_ascii=False)+';\n')

import hashlib
assert hashlib.sha256((P('docs')/p['texte']['fonte_fichier']).read_bytes()).hexdigest()==p['texte']['fonte_sha256']
