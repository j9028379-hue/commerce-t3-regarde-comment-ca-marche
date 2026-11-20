import json,hashlib,sys,zipfile,tempfile
from pathlib import Path as P
from jsonschema import validate
ROOT=P(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'package'));from livrer import verify
J=lambda p:json.loads(P(p).read_text());e=J('catalogue/catalogue.json')['entries'][0];s=J(e['contrat']);validate(s,J('schemas/template.json'));v=J(e['audio']);q=J(e['formulaire'])['champs'];g=J(e['cartes'])['ecrans'];gold=J('golden/job.json');validate(gold,J(e['schema_job']));assert e['audio_profile']==s['audio_profile']==v['id'] and v['mix_approuve'] and v['voix_approuvee'];assert {x for keys in s['texte']['liaison_champs'].values() for x in keys}==set(gold['reponses'])=={c['cle'] for c in q};assert [r['numero'] for r in g]==gold['ecrans'];assert gold['reponses']==J('render/demo/reponses.json');assert hashlib.sha256(P('docs/media/COMMERCE-T3-Boutique-Elegance-07.mp4').read_bytes()).hexdigest()==J('approvals/validation.json')['master_sha256'];assert hashlib.sha256(P(v['voix_demo']).read_bytes()).hexdigest()==J('approvals/validation.json')['voix_sha256'];print('PASS canon, formulaires, cartes, golden, master 07, voix, mix')
if len(sys.argv)>1:
 z=sys.argv[1];m=verify(z)
 with tempfile.TemporaryDirectory() as d:
  bad=P(d)/'alteration.zip'
  with zipfile.ZipFile(z) as src,zipfile.ZipFile(bad,'w') as dst:
   for n in src.namelist():dst.writestr(n,src.read(n)+(b' ' if n==e['contrat'] else b''))
  try:verify(bad)
  except AssertionError:pass
  else:raise AssertionError('Paquet altéré accepté')
 print('PASS ZIP, crédits et rejet de la modification')
