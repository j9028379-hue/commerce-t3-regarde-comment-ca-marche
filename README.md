# COMMERCE-T3 · Regarde comment ça marche · 1.0.0

[Parcours](https://j9028379-hue.github.io/commerce-t3-regarde-comment-ca-marche/) · [Film de référence](docs/film.html) · [Contrat de montage](montage/partition.json) · [Décision et empreintes](approvals/validation.json) · [Audit Actions](../../actions/workflows/parite.yml).

La carte T3 est une entrée de `catalogue/catalogue.json`, pas une nouvelle application. Sa version relie le formulaire, les cartes de tournage, la partition, le profil audio et le paquet distribuable. `tools/site.py` génère `docs/data.js`; ne pas éditer la copie. Le job du navigateur contient les six réponses (prix facultatif), la version, les 12 étapes et les empreintes des quatre prises. Chaque titre commercial vient de `texte.liaison_champs`. Les indications de tournage ne deviennent pas des slogans dans le film.

## Livrer un film marchand

1. Remplir le formulaire, parcourir A/B/C pour chaque scène (6, 8, 7, 9 s), relire et valider quatre vidéos. Exporter dans un dossier `job.json`, `S1.mp4` à `S4.mp4`. Utiliser des MP4 lisibles comportant au minimum la durée guidée. Utiliser le lien dédié à chaque prise. L’aperçu de mouvement illustré est distinct du film approuvé sur prises réelles.
2. Sur Linux, fournir Python 3.12 (`numpy`, `opencv-python-headless`, `jsonschema`), FFmpeg/ffprobe, Node 22, `puppeteer-core@23.11.1` dans `NODE_PATH` et Chrome à `/usr/bin/google-chrome`. Exécuter `python render/marchand.py --job /chemin/entree --out /chemin/livraisons --state /chemin/durable/t3.sqlite`. Garder **la même base et le même dossier de livraisons** sur une machine hôte ; ne pas recréer l’état entre deux clients. Une base locale distincte par runner ne serait pas une rotation globale.
3. Chaque succès fournit `Film.mp4`, `RenderResult.json`, `CREDITS.txt`, les titres et les contrôles. L’échec produit un `RenderError-*.json`, sans consommer de piste. L’empreinte du job sert d’identifiant de reprise. L’audio marchand provient des prises, sur leur scène respective ; sinon musique seule. Pas de voix « Boutique Élégance » injectée chez un autre marchand.
4. Cycle strict 1→2→3→4→1, après succès, avec verrou transactionnel et contrôle des sources. Les quatre extraits CC BY 4.0 sont redistribuables avec crédits. `audio/CREDITS.md` pour le paquet, crédit de la piste et modifications pour chaque film. La narration et les quatre mix d’exemple restent dans `render/demo/`, hors du chemin marchand.

## Référence et limites d’intégration

T1 : `vitrine-video-gabarits` branche `feat/commerce-t1-silencieux` @ `186e46a` (runtime, schémas, golden, paquet, couche de contrôle). T2 : `commerce-t2-nouvel-arrivage` @ `ae2d3b3` (job navigateur, moteur marchand, test d’une autre saisie, dry-run Wrangler, manifeste). Parité **fonctionnelle**, pas interchangeabilité binaire. Voir `qc/parite.py`, `qc/temoin.py`, `qc/test-audio-local.py` et le workflow `parite.yml`.

Le Worker de référence expose en GET `/v1/health`, `/v1/catalogue` et `/v1/templates/COMMERCE-T3/1.0.0`. Il refuse les écritures. Wrangler est compilé en dry-run : pas de compte, secrets, domaine, R2, déclencheur de rendu public ni publication OTA. Pages ne filme pas avec une caméra physique et ne téléverse pas les fichiers privés. L'intégration dans une app commune de production est une étape distincte.

`python package/livrer.py build /chemin/COMMERCE-T3-1.0.0.zip` depuis le dépôt Git, puis `python package/livrer.py verify /chemin/COMMERCE-T3-1.0.0.zip`. Le manifeste vérifie l’intégrité, pas la signature d’un éditeur. Sources visuelles de démo et licences : `render/demo/plans-filmes.json`, crédits et OFL dans le paquet. Ne pas confondre les anciens essais techniques archivés avec le master 07 approuvé.
