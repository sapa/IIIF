# Projet IIIF / Erismann

Le fonds Fred Erismann est un fonds de photographies prises par la photographe Fred Erismann entre 1934 et 1968. Ces images documentent les productions théâtrales du Stadttheater Berne. La plupart de ces images sont sous forme de négatifs. Pour plus de détail voir la notice de fonds : http://data.performing-arts.ch/r/ed267524-673e-43b3-8037-1e3c833d8b02.
## Description
La description a été faite au niveau du dossier = production, plus à l'intérieur de ceux-ci le choix d'une ou deux images représentatives.
## Numérisation
Les images représentatives retenues ont été numérisées, y sont inclus une série de [métadonnées embarquées](Embeded-Metadata-Erismann). 
## Ingest 
### Métadonnées descriptives (I)
Les images retenues sont donc décrites sous la forme suivante :
-record Set
  - record
    - instantiation : Archival Master (AM)
    - instantiation : Preservation Copy (PC)
    - instantiation : Dissemination Copy (PC-DC)
### Images numérisées
1. Les PC sont versés dans le dépôts d'archivage numérique (docuteam Cosmos)
2. leurs PID ajoutés au métadonnées descriptives.
3. Les PC sont transformées en DC (selon le format à définir)
4. Les DC sont versé sur le serveur d'images IIIF de SAPA
5. Les URL des DC sont ajoutés au métadonnées descriptives
6. Les URL des manifestes (non existants encore) sont ajoutées aux métadonnées descriptives.
### Métadonnées descriptives (II)
1. Livrées sous forme CSV (avec PID et URL des DC), les métadonnées descriptives ne sont pas ingestées dans le dépôt d'archives numériques. Elles sont transformées en JSON-LD et importées dans la plateforme perfoming-arts.ch (SPAP).
### Manifest
1. On va créé les Manifest IIIF (voir [Manifest-Erismann](Manifest-Erismann)) en tirant des informations de :
-  des notices SPAP (URL)
-  les métadonnées embarquées
2. Déposer les Manifestes sur le serveur.

