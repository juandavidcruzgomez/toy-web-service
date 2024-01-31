# Utilisation de dvc pour controller les modèles et les données - P2
## 1. Configurer un environnement virtuel sur `dag-demo`
On va commencer pour faire `git pull` pour être surs d'avoir la bonne version.
Ensuite, on va executer :
```bash
python -m venv ~/dag-demo
```
(Modifier selon l'emplacement du dossier dag-demo)
et ensuite, on va activer l'environnement virtuel :
```bash
source ~/dag-demo/bin/activate
```
Maintenant, nous avons un environnement local pour installer des packages sans impacter l'environnement global.
C'est obligatoire ? Non, on peut aussi installer dvc de manière globale.
## 2. Installer dvc
Exécutes
```bash
pip install dvc
```
C'est tout

## 3.  Créer une nouvelle branche dans le projet
Dans notre projet `dag-demo` executes :
```bash
git checkout -b first_experiment_ton_nom
```
## 4. Initialiser dvc
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
.dvcignore
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
dvc add data/raw/train
dvc add data/raw/val
```
Maintenant, on va ajouter les fichiers dvc à git :
```bash
git add data/raw/.gitignore data/raw/train.dvc
git add data/raw/val.dvc data/raw/.gitignore
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
rm -rf data/raw/val
```
Les données de validation sont supprimées du disque. On peut les récupérer depuis le cache :
```bash
dvc checkout app/data/raw/val.dvc
```
Si les données ne sont pas dans le cache, il faut utiliser `fecth` et ensuite `checkout`.
## 4. On va ajouter le modèle au repo dvc
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
Maintenant, nous avons nos données et notre modèle contrôlées.
Push
```bash
git pull # et ressoudre les conflits
git push
dvc push
```

### 5. Changer les paramètres du modèle
Crée une nouvelle branche :
```bash
git checkout -b "sgd-1000-iterations-ton_nom"
```
Modifie le code du `training.py` dans le dossier des DAGs (met par exemple `max_iter=1000`).
Relance le DAG sur airflow.
Une fois que le workflow est fini, on doit avoir une nouvelle version du modèle avec une accuracy changée.
Commit sur dvc
```bash
dvc commit
```
Commit et push le code aussi avec git, fais
```bash
dvc push
```
## 6. Changer de branche
Maintenant nous avons deux versions du modèle. On peut basculer entre les deux en utilisant la commande checkout de git et de dvc.
```bash
git checkout first_experiment_ton_nom
dvc checkout
```
Comme ça, dvc va placer la version du modèle de la branche `first_experiment_ton_nom` dans notre volume.
L'application continue à utiliser le modèle disponible dans le volume.
