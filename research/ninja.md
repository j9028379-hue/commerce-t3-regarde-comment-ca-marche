# Ninja Blast Max : lecture du clip choisi

Mesures sur le clip source de 562 images à 30 i/s, en **720 × 900 (4:5)**, et non 9:16. Seul le gabarit cible est vertical 9:16. Les médias, la marque et les textes de la publicité ne sont pas importés.

| Images originales, index à partir de zéro | Observation | Adaptation T3 |
|---|---|---|
| 0–92 | Produit centré ; changements secs de décor/variante aux images 14, 27, 40, 54. Premier titre déjà présent ; second titre blanc sur deux lignes en fondu. | S1, 0–6 s : même produit et même axe. Texte du commerçant, jamais celui du spot. |
| 93–302 | Passage sec à quatre cases ; vues synchronisées ; texte blanc centré à cheval sur la séparation ; vagues de lettres avec rotation et changement d’échelle, puis lecture à plat. | S2, 6–14 s : quatre cadrages d’une seule prise. Pas quatre articles à filmer. |
| 303–470 | Retour sec au plein cadre ; à partir de 303 les lettres entrent en cascade, première ligne puis seconde, et se stabilisent. Changements d’environnement, notamment aux images 327, 351, 375, 399. | S3, 14–21 s : le cadre revient d’un coup ; garder le geste entier. Décaler les accents de décor en S4 pour protéger l’action. |
| 471–561 | Produit isolé et variantes en plein cadre ; texte blanc, puis sortie sur une vue stable. | S4, 21–30 s : montrer le vrai résultat, le prix seulement si renseigné, puis le contact. |

**Typographie :** sans empattement géométrique, grasse, en casse de phrase, non condensée (observer au ratio natif). Le nom du fichier de police original n’est pas établi. Montserrat Bold est un substitut local sous OFL, pas une identification de la police Ninja. Les lettres progressent de gauche à droite avec une queue plus petite, inclinée, sous la ligne de base. La maquette de mouvement est un test sur lampe dessinée, pas des prises réelles ni une publicité finalisée.

## Révision 02 — la dérive rotative n’est pas un fondu

La capture fournie correspond à la deuxième ligne en cours d’entrée vers les images 106–108 du film source : la première ligne est presque posée tandis que les derniers caractères de la deuxième arrivent encore minuscules en bas à droite. Sur le Y initial, segmentation du blanc et ajustement à la silhouette posée vers l’image 120 : image 96 ≈ +12/+74 px, rotation +54°, échelle 0,52 ; image 103 ≈ −7/−15 px, −13°, échelle 1,10 ; image 111 ≈ repos. Les plus petites silhouettes sont approximées. Les paramètres reconstruits sont explicités dans `montage/partition.json`. Le JSON de projet propriétaire et la police source ne sont pas disponibles.

Intro : raccords secs. Grille : bordure noire de 6 px, deux lignes de part et d’autre de la jonction, quatre cadrages et deux changements secs à l’intérieur de la grille. Retour en plein cadre : transitions de décor sans interrompre l’action. Le moteur du site et le générateur des titres MP4 lisent les mêmes clés du JSON. L’étalonnage atténue le jaune de la prise ; ab et non la luminance changent pour teinter le décor. Pas de calque jaune. Les rushes et le scénario restent ceux du test de cafetière, pas de réemploi des images Ninja.
