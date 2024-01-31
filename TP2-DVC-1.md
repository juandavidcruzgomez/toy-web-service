# Utilisation de dvc pour controller les modèles et les données - P1
## 1. Reconfigurer airflow pour utiliser `scikit-learn`et `scikit-image`
Nous avons déjà déployé `airflow` en local. Nous avons aussi vu comment écrire des DAGs basiques pour implémenter des workflows (ou des pipelines). 
Maintenant, nous voulons implémenter des tâches de préparation, entraînement et validation pour un modèle de classification simple d'images.
On va commencer pour arrêter tous les conteneurs `airflow`. Si les conteneurs ne sont pas en mode détaché (lancés avec `docker compose up`) il suffit de faire `ctrl+c`.
Si les conteneurs sont en mode détaché (lancés avec `docker compose up -d`), il faut faire `docker compose stop`. Ou sur Docker desktop.
Ensuite, il faut spécifier l'image `airflow` à utiliser  pour le docker compose. Dans la ligne 52 du fichier `docker-compose.yml` on peut voir qu'il est possible de spécifier l'image à travers d'une variable d'environnement  :
```
image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.8.1}
```
Alors, on peut relancer notre fichier `docker-compose.yml` avec une petite variation :
```bash
AIRFLOW_IMAGE_NAME=juandavidcruzgo/airflow:2.8.1-custom docker compose up
```
Cela va définir la variable d'environnement avant de lancer docker compose.
**Note : ici on utilise une image de hub.docker.com. Il est possible de builder une image en local sans la télécharger**
Maintenant, on peut utiliser ces deux bibliothèques avec nos DAGs.
## 2. Relire le code du projet
Voici la structure du projet :
```
imt
├─ __init__.py
└─ classification_simple_demo
   ├── __init__.py
   ├── classification_simple.py
   ├── prepare_task.py
   ├── train_task.py
   └── validation_task.py
```
Dans le dossier `imt/classification_simple_demo` il y a le code nécessaire pour exécuter les tâches de préparation des données, entraînement et évaluation du modèle. Le DAG est définie dans le fichier `classification_simple.py`. 
## 2. Récupérer les données
Dans le dossier `dag-demo`, lance :
```bash
bash download-data.sh
```
Ceci lance un script qui va télécharger les données du jeu *imaginette*. Ce jeu de données contient des images pour implémenter des tâches de classification. Tu peux trouver plus d'information [ici](https://github.com/fastai/imagenette).
Le jeu de données contient 3 sous-ensembles : 
- Full size
- 320px
- 160px
Par soucis de taille nous allons utiliser l'ensemble 160px.
Les données téléchargées par le script sont copiées dans le dossier `data/raw` où elles sont divisées en `train` pour les tâches d'entraînement et `val` pour les tâches de validation des modèles.
## 3. Exécuter les tâches de classification
Une fois les données téléchargées, on peut lancer les tâches.
Sur l'interface [airflow](http://localhost:8080),  cherches le DAG `classification_basic_1` et cliques sur lui. Tu verras les tâches du DAG, tu peux voir aussi le graph des tâches.
Cliques sur le bouton play en haut à droite pour lancer le DAG.
La tâche `preparation` va générer deux fichiers csv (stockés dans `data/prepared`) . Ces fichiers vont être utilisés par la tâche `training` pour avoir les étiquettes. Ci-dessous un example de la structure du fichier d'entraînement :

| id | path | class |
| :----: | :----: | ---- |
| 0 | /opt/airflow/data/raw/train/n03445777/n03445777_5768.JPEG | golf ball |
| 1 | /opt/airflow/data/raw/train/n03445777/n03445777_2557.JPEG | golf ball |
| 3 | /opt/airflow/data/raw/train/n03445777/n03445777_237.JPEG | golf ball |
L'entraînement est fait de manière supervisée.
Une fois l'entraînement est fini, la tâche de validation (`evaluation`) est lancée. L'évaluation va donc prendre le fichier `data/prepared/test.csv` et utiliser le modèle généré pour vérifier sa qualité.

## 4. Tester l'application web
Télécharger l'image de dockerhub et lancer le conteneur :
```bash
docker run -p 8000:8000 -v ~/dag-demo/models:/var/web/models juandavidcruzgo/toy-web-application:1.0.0
```
Si tout est OK, on doit avoir un serveur d'application web qui tourne sur le port 8000 de la machine. On peut tester [ici](http://localhost:8000)
C'est une application web python qu'utilise FastAPI (on peut aussi faire avec Flask par exemple) et qui va utiliser le modèle que nous avons entraîné avec le DAG airflow et qui est sauvegarde dans le dossier `dag-demo/models`.
Pour ce faire, nous avons indiqué à docker d'utiliser un volume qui pointe vers ce dossier.
Cela veut dire que si nous changeons le modèle, l'application (après redémarrage) va récupérer la nouvelle version sans trop de complication.
