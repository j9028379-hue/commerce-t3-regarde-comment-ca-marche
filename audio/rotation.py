"""État par gabarit : le rendu lit la dernière piste livrée. Ne valider qu'après succès."""
def prochaine(profil, derniere=None):
    ids=profil['pistes_approuvees']
    if len(ids)!=4 or len(set(ids))!=4 or not profil['mix_approuve'] or not profil['voix_approuvee']:
        raise ValueError('Pack non validé')
    if derniere is None:return ids[0]
    return ids[(ids.index(derniere)+1)%4]

import sqlite3
from pathlib import Path
import hashlib

def livrer(db,profil,job,produire):
    """État SQLite durable à partager entre rendus du profil. Callback: préparer la livraison de façon idempotente ou lever une exception."""
    if not job: raise ValueError('Job requis')
    con=sqlite3.connect(db, timeout=120)
    try:
        con.execute('BEGIN IMMEDIATE');con.execute('CREATE TABLE IF NOT EXISTS livraisons(seq INTEGER PRIMARY KEY, profil TEXT, job TEXT, piste INTEGER, UNIQUE(profil,job))');scope=profil['id'];old=con.execute('SELECT piste FROM livraisons WHERE profil=? AND job=?',(scope,job)).fetchone()
        if old:return old[0]
        last=con.execute('SELECT piste FROM livraisons WHERE profil=? ORDER BY seq DESC LIMIT 1',(scope,)).fetchone();n=prochaine(profil,last[0] if last else None);t=next(t for t in profil['pistes'] if t['numero']==n);p=Path(__file__).resolve().parents[1]/t['fichier'];assert hashlib.sha256(p.read_bytes()).hexdigest()==t['extrait_sha256'];produire(p,t['credit']);con.execute('INSERT INTO livraisons(profil,job,piste) VALUES (?,?,?)',(scope,job,n));con.commit();return n
    finally:con.close()
