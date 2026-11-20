"""Job exporté par le navigateur + 4 prises → livraison atomique par job. Aucun upload."""
import argparse,hashlib,json,os,shutil,subprocess as sp,sys,tempfile
from pathlib import Path as P
from jsonschema import validate
ROOT=P(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'audio'));from rotation import livrer;from mixer import marchand,H
J=lambda p:json.loads(P(p).read_text())
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def run(src,dest,db):
    src,dest,db=map(lambda p:P(p).resolve(),(src,dest,db));dest.mkdir(parents=True,exist_ok=True);stage='JOB'
    try:
        job=J(src/'job.json');validate(job,J(ROOT/'schemas/render-job.json'));clips=[src/(c['scene']+'.mp4') for c in job['captures']];assert len(set(c['sha256'] for c in job['captures']))==4 and all(H(p)==c['sha256'] for p,c in zip(clips,job['captures'])),'Prises différentes de celles validées dans le formulaire';catalog=J(ROOT/'catalogue/catalogue.json')['entries'][0];plan=J(ROOT/catalog['contrat']);profil=J(ROOT/catalog['audio']);assert job['template_version']==catalog['version']==plan['version']==profil['version'];jid=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest();final=dest/jid;db.parent.mkdir(parents=True,exist_ok=True);stage='MONTAGE'
        def produire(music,credit):
            nonlocal stage
            with tempfile.TemporaryDirectory(dir=dest) as tmp:
                w=P(tmp);out=w/'livraison';out.mkdir();work=w/'work';work.mkdir()
                for name in ['docs','capture-guide','schemas','montage']:(w/name).symlink_to(ROOT/name,target_is_directory=True)
                for p in clips:(work/p.name).symlink_to(p)
                dump(out/'job.json',job);env={**os.environ,'T3_MARCHAND':'1'}
                for cmd in [['node',str(ROOT/'render/titres.cjs')],[sys.executable,str(ROOT/'render/film.py')]]:sp.run(cmd,cwd=w,env=env,check=True)
                stage='AUDIO';track=next(t for t in profil['pistes'] if ROOT/t['fichier']==music);credit+=' Adaptation : mixage avec le son des prises, atténuation sous la parole.';report=marchand(out/'COMMERCE-T3-Regarde-comment-ca-marche.mp4',clips,plan['scenes'],profil,music,credit,out/'Film.mp4');(out/'CREDITS.txt').write_text(credit);dump(out/'audio.json',report);rr=dict(status='COMPLETED',template_id=job['template_id'],run_id=jid,output='Film.mp4',music_id=track['numero'],sha256=H(out/'Film.mp4'));validate(rr,J(ROOT/'schemas/render-result.json'));dump(out/'RenderResult.json',rr)
                if final.exists():
                    previous=J(final/'RenderResult.json');assert previous==rr and H(final/'Film.mp4')==rr['sha256'],'Sortie existante en conflit'
                else:os.replace(out,final)
        pick=livrer(db,profil,jid,produire);r=J(final/'RenderResult.json');assert r['music_id']==pick and H(final/'Film.mp4')==r['sha256'];return r
    except Exception as exc:
        err=dict(status='FAILED',stage=stage,message=str(exc)[:500] or 'Contrôle refusé');validate(err,J(ROOT/'schemas/render-error.json'))
        with tempfile.NamedTemporaryFile(mode='w',dir=dest,prefix='RenderError-',suffix='.json',delete=False) as f:json.dump(err,f,ensure_ascii=False)
        return err
if __name__=='__main__':
    p=argparse.ArgumentParser();[p.add_argument('--'+k,required=True) for k in ('job','out','state')];o=p.parse_args();r=run(o.job,o.out,o.state);print(json.dumps(r,ensure_ascii=False));sys.exit(r['status']!='COMPLETED')
