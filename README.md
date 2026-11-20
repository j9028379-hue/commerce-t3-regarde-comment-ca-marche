# COMMERCE-T3 — Regarde comment ça marche

**Référence choisie : Ninja Blast Max.** [Parcours des six questions et douze écrans](https://j9028379-hue.github.io/commerce-t3-regarde-comment-ca-marche/) · [Lire l’étude visuelle de 30 secondes](https://j9028379-hue.github.io/commerce-t3-regarde-comment-ca-marche/apercu.html).

[Décision et empreinte source](approvals/reference.json) · [Analyse image par image des principaux raccords](research/ninja.md) · [Partition de 900 images](montage/partition.json) · [Animation des titres](docs/motion.js).

[Questions](form/questions.json) : prix facultatif, question 4 sur la démonstration. [Textes des 12 écrans](capture-guide/ecrans.json) : A guide, B enregistrement, C vérification, 6/8/7/9 s. `python tools/site.py` synchronise ces fichiers avec le site. Maquette locale de saisie/relecture : pas de caméra ni de montage marchand exécuté par le site. L’étude animée, distincte du formulaire, utilise une lampe dessinée et des données fictives. La fonte de substitution est fournie sous OFL. Pas de republication d’images de la campagne, de musique ou de voix validée.

## Rendu silencieux sur GitHub Actions

Le parcours complet (et non la visite libre) peut désormais exporter `job.json` après validation de quatre fichiers distincts. Le workflow manuel `rendu-silencieux.yml` utilise l'interface dans Chrome, importe quatre rushes Mixkit vérifiés, puis assemble le MP4 selon `montage/partition.json`, avec le moteur de lettres de l’aperçu. Les réponses de la démonstration (atelier et contact fictifs) sont dans `render/demo/reponses.json`, les références de licence et les empreintes dans `render/demo/rushs.json`. Démonstration : verser l’eau sur le café dans une cafetière à piston ; le prix est volontairement vide. Pas de prise son, de mélangeur audio ni de piste muette ; le conteneur a uniquement un flux vidéo. Le rendu est un workflow séparé, pas un envoi automatique des vidéos des visiteurs de Pages.

Pour conserver poignée, couvercle et base en scène 1, le moteur recale les bandes réellement filmées du panoramique de la prise 1 avant le raccord de couleur. La scène 3 est un versement continu ; dans ce jeu de rushes, le bec verseur et le filet d’eau sont visibles, pas la main entière.
