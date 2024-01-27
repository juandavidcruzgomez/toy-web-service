# Utilisation de dvc pour controller les modèles et les données
## 1. Relire le code du projet
Voici la structure du projet :
```
toy-web-service
├── LICENSE
├── README.md
├── TP1-CONFIG.md
├── TP2-DVC.md
└── app
    ├── cleanup.sh
    ├── data
    ├── download-data.sh
    ├── main.py
    ├── metrics
    ├── models
    ├── requirements.txt
    └── src
        └── ml-tasks
            ├── steps
            │   ├── evaluate.py
            │   ├── helper.py
            │   ├── prepare.py
            │   └── train.py
            └── train_pipelines.py
```
Dans le dossier `src/ml-tasks` il y a le code nécessaire pour exécuter les tâches de préparation des données, entraînement et évaluation du modèle. Le fichier `train_pipelines.py` execute les trois tâches.
Le fichier `main.py` lance le serveur web avec FastAPI. Le fichier `requirements.txt`contient les bibliothèques python à installer pour ce TP.
Les autres dossiers (`models`, `metrics` et `data`) on va les voir plus loin.
## 2. Récupérer les données
Dans le dossier `toy-web-service/app`, lance :
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
Lance
```bash 
cd app
python src/ml-tasks/train_pipelines.py
```
Ceci va exécuter les tâches de préparation, entraînement et validation. 
La tâche de préparation (fichier `steps/prepare.py`) va créer les jeux de données d'entraînement et de validation. Ils sont stockés dans les dossier `data/prepared`.
Ensuite, la tâche d'entraînement (fichier `steps/train.py`) va utiliser le fichier `data/prepared/train.csv` pour configurer et entraîner un modèle de classification. Une fois ce modèle entrainé, il est stocké dans le dossier `app/models/model.joblib`.
Finalement, la tâche d'evaluation (fichier `steps/evaluate.py`) va tester le modèle entraîne précédemment avec les données de validation. À la sortie, elle va écrire dans le fichier `app/metrics/accuracy.json` le pourcentage de données bien classifiées. 
## 4. Tester l'application web
Oui, quand même !
