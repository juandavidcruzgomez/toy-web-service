# Utilisation de dvc pour controller les modèles et les données - P2

## 1.  Créer une nouvelle branche dans le projet
Dans notre projet `toy-web-app` executes :
```bash
git checkout -b first_experiment
```
## 2. Initialiser dvc
Il faut vérifier que dvc est bien installé. Executes `dvc version` , si  le résultat est quelque chose comme `dvc: command not found`, il faut installer dvc avec `pip`.
Si tout est OK, on peut initialiser le repo dvc
```bash
dvc init
```
Ceci va créer la structure du projet dvc (quelque chose comme ça) :
```bash
.dvc
├── config
└── tmp
    ├── btime
    ├── dag.md
    ├── exps
    │   ├── cache
    │   │   ├── 7e
    │   │   │   └── dd66472694ea6af8e8717a0376b742a4f5ca77
    │   │   ├── bf
    │   │   │   └── 11700ebcd3eaa526283c50879e969d594cac2b
    │   │   └── f3
    │   │       └── 79914dd12126bf88ce6df6980c6ba7b90007de
    │   └── celery
    │       ├── broker
    │       │   ├── control
    │       │   ├── in
    │       │   └── processed
    │       └── result
    ├── updater
    └── updater.lock
.dvcignore  [error opening dir]
```
Maintenant, nous allons configurer un stockage pour nos données. Nous allons utiliser un stockage local
```bash
mkdir -p ~/dvc-demo/remote_data_repo
dvc remote add -d remote_storage ~/dvc-demo/remote_data_repo
```
Il s'appelle "remote" même si pour cette exemple il est local. DVC permet de configurer différents types de stockage, entre autres :
- AWS S3
- Google Cloud Storage
- Azure Blob Storage
- Google drive
Vérifie le contenu du fichier config dans `.dvc`
## 3. Ajouter les données au repo dvc
Maintenant, nous allons tracker les données. Toujours dans la racine du projet exécutes :
```bash
dvc add app/data/raw/train
dvc add app/data/raw/val
```
Maintenant, on va ajouter les fichiers dvc à git :
```bash
git add app/data/raw/.gitignore app/data/raw/train.dvc
git add app/data/raw/val.dvc app/data/raw/.gitignore
git add --all
```
On est prêts pour faire un commit git :
```bash
git commit -m "First data commit with dvc"
```
Et ensuite on peut *pusher* les données :
```bash
dvc push
```
Ceci va mettre les données dans notre stockage remote § 2.
Finalement, push tout à git
```bash
git push --set-upstream origin first_experiment
```
Alors, on peut maintenant supprimer les données ?
Oui, mais il faut faire attention a ne pas supprimer les fichiers dvc. Pour essayer :
```bash
rm -rf app/data/raw/val
```
Les données de validation sont supprimées du disque. On peut les récupérer depuis le cache :
```bash
dvc checkout app/data/raw/val.dvc
```
Si les données ne sont pas dans le cache, il faut utiliser `fecth` et ensuite `checkout`.
## 4. Entraîner un modèle de classification et ajouter le modèle au repo
Sur `app`  exécutes :
```bash
python src/ml_tasks/train_pipelines.py
```
Cela va prendre les données d'entraînement et validation pour créer un modèle de classification qui utilise une approche de Gradient Descendant (SGDClassifier de ScikitLearn).
Ce pipeline contient trois étapes : 
1. Préparation des données (`prepare.py`): création des fichiers csv (`app/data/prepared/train.csv` et `app/data/prepared/test.csv`) pour les phases d'entraînement et de validation.
2. Entraînement (`train.py`) :  utilise les données d'entraînement pour créer le modèle. Il sera stocké dans `app/models/model.joblib`.
3. Validation (`validate.py`) : charge le modèle entraîné et utilise les données de test pour vérifier son accuracy. Le résultat est stocké dans `app/metrics/accuracy.json`.
On va ajouter des fichiers a dvc. D'abord les données d'entraînement :
```bash
dvc add data/prepared/train.csv data/prepared/test.csv
git add -all
git commit -m "Training and validation files created"
```
Ensuite, le modèle :
```bash
dvc add models/model.joblib
git add --all
git commit -m "Model trained using SGDClassifier"
```
Et finalement, le fichier d'accuracy :
```bash
git add metrics/accuracy.json 
git commit -m "Accuracy of SGDClassifier"
```
