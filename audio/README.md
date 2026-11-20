# Audio T3 • pack musical 01

Le catalogue référence `audio/profil.json`, avec les quatre extraits de 30 s effectivement approuvés. Ils commencent sur une attaque : les points d’entrée sont déjà appliqués, ne pas les appliquer à nouveau. Pas de piste Pixabay. Voir [les crédits obligatoires](CREDITS.md).

Rotation séquentielle par profil : `rotation.livrer(db, profil, job_id, produire)`. Le callback reçoit le MP3 et le crédit à joindre au film. Il doit préparer une sortie idempotente par identifiant de job et lever une exception si le rendu ou ses contrôles échouent. Un échec ne consomme pas de piste. Le chemin SQLite doit être durable et commun aux livraisons (pas un fichier temporaire recréé par runner). La CI teste ce comportement ; aucun stockage de production n’est provisionné. Le chemin sonore reste bloqué tant que voix et mix ne sont pas approuvés. Ne pas modifier le film muet.

Parité T1/T2 : même séparation catalogue/contrat/état, Worker de référence en lecture seule. T3 adopte l’ordre 1→2→3→4 plutôt que le tirage à exclusion de T2. Étape suivante : écoute voix seule puis mix avec baisse musicale sous la parole. Ni déploiement Cloudflare ni OTA à ce stade.
