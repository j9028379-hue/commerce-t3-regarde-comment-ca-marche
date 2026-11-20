from pathlib import Path
import json,sys
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'audio'));from rotation import prochaine
read=lambda p:json.loads((root/p).read_text());e=read('catalogue/catalogue.json')['entries'][0];p=read(e['audio']);assert e['audio_profile']==p['id'] and e['template_id']==read(e['contrat'])['template_id']
assert prochaine(p)==1
try:prochaine(dict(p,mix_approuve=False))
except ValueError:pass
else:raise AssertionError('Audition activée')
fixture=dict(p,pistes_approuvees=['A','B','C','D'],voix_approuvee=True,mix_approuve=True);last=None
for n in range(10000):
    s=prochaine(fixture,last);assert s!=last and s=='ABCD'[n%4] and prochaine(fixture,last)==s;last=s
print('PASS : contrat → profil ; pack approuvé, blocage des profils non validés ; 10 000 sélections cycliques simulées')
from rotation import livrer
from tempfile import TemporaryDirectory
from concurrent.futures import ThreadPoolExecutor
import hashlib
assert p['pistes_approuvees']==[t['numero'] for t in p['pistes']]==[1,2,3,4]
for t in p['pistes']:assert hashlib.sha256((root/t['fichier']).read_bytes()).hexdigest()==t['extrait_sha256'] and 'CC BY 4.0' in t['credit']
with TemporaryDirectory() as tmp:
    db=Path(tmp)/'test.sqlite';mock=dict(p,voix_approuvee=True,mix_approuve=True);noop=lambda *_:None
    try:livrer(db,mock,'a',lambda *_:(_ for _ in ()).throw(IOError('échec simulé')))
    except IOError:pass
    for i,v in enumerate([1,2,3,4,1]):assert livrer(db,mock,str(i),noop)==v
    with ThreadPoolExecutor(4) as pool:assert list(pool.map(lambda _:livrer(db,mock,'unique',noop),range(4)))==[2]*4
    assert livrer(db,mock,'suivant',noop)==3
print('PASS : quatre MP3 validés, SHA-256, crédits, reprise, idempotence et accès concurrents')
