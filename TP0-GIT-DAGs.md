# Introduction rapide à git et DAGs avec Airflow
## 1. Intro à git
### 1.1 Installation
Si jamais, tu n'a pas git installé sur ta machine...
[Guide d'installation de git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)
Testes l'installation :
```bash
git --version
```
Tu dois avoir un message comme celui-ci : `git version 2.39.2 (Apple Git-143)` (selon la machine cela peut changer...) mais en tout cas, l'idée est de ne pas avoir une erreur.
### 1.2 Cloner un repository
C'est la première opération à faire pour initialiser un repository en local. Cette commande va récupérer l'information (code, configurations et autres fichier de texte) et va créer les liens vers le repository central.
Pour démarrer le processus il faut tout simplement exécuter :
```bash
git clone https://github.com/juandavidcruzgomez/dag-demo.git
```
Ceci va créer un dossier `dag-demo` avec trois fichiers :
- docker-compose.yml
- download-data.sh
- README.md
Maintenant, on peut exécuter 
```bash
git status
```
pour vérifier le status du repo local. Si l'on vient de faire le clone, on doit avoir un message comme
```
On branch main
Your branch is up to date with 'origin/main'.
``` 
### 1.3 Modifier un fichier
Maintenant, on va modifier le fichier `README.md` (ce type de fichiers utilisent le format MarkDown).
Ouvre le fichier dans un editor/IDE, et ajoute après la ligne `## Liste d'assistents au cours :`
l'information suivante :
`- Nom PRENOM`
Sauvegarde le fichier, et ensuite, tu peux vérifier l'état de ton repo local avec `git status`. Tu dois avoir quelque chose comme cela :
```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md
```
Remarques l'indication comme quoi README.md a été modifié.
Ensuite, il faut ajouter le fichier à la liste de commit. Exécute 
```bash
git add README.md
```
**Note : il es possible d'utiliser `git add --all` pour tout ajouter, mais cela peut créer des problèmes**
On est prêts pour faire un commit : on prend responsabilité pour le code.
```bash
git commit -m"Un commentaire qui explique le contenu du commit. Certains met des emojis 😆"
```
Et maintenant, on peut _pusher_ au repo central. Mais avant, on va récupérer la dernière version :
```bash
git pull
git push
```
Et c'est tout ? Non, la commande `git pull` peut récupérer des fichiers qui vont rentrer en conflit avec notre version, et ça, il faut le résoudre.
Mais si tout se passe bien, on doit avoir un message similaire à 
```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 373 bytes | 373.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
To github.com:juandavidcruzgomez/dag-demo.git
   498a330..e7d7b6a  main -> main
```
## 2. Intro aux DAGs avec Airflow
Un DAG (Direct Acyclic Graph) dans le contexte de ML define une liste de tâches exécutées de manière séquentielle pour manipuler des données et/ou exécuter des tâches d'apprentissage;
[Apache Airflow](https://airflow.apache.org/) est une plateforme écrite en python qui permet d'exécuter de workflows asynchrones, typiquement pour de tâches associées à la gestion et manipulation de données.
Pour faciliter l'installation, on va utiliser Docker.
### 2.1 Fichier `docker-compose.yml`
Ce fichier contenu dans notre repo va nous aider à automatiser et lancer les tâches un peu pénibles de la configuration d'Airflow : Airflow utilise deux bases de données de backend, redis et postgresql. En plus, airflow lance plusieurs conteneurs spécialisés. 
**Attention ! cette installation n'est pas convenable pour un environnement de production. Elle n'est pas sécurisée !**
Le fichier commence (ligne 47) par définir des configurations communes aux services airflow. Par exemple, dans la ligne 114, nous avons l'instruction suivante : `<<: *airflow-common`.
Cerci indique à docker qu'il doit injecter la configuration de airflow-common pour le service `airflow-webserver` .
Dans ce fichier, dans les lignes 73 à 76 nous trouvons la définition de volumes laquelle a la structure suivante
`path_local_file_system:path_container_file_system`
Par exemple, si j'ai un volume définit comme :
`/home/juan/docker-data:/var/web/data`
cela indique que le conteneur va monter le dossier de ma machine (ou le serveur) `/home/juan/docker-data` dans `/var/web/data` à l'intérieur du conteneur.
### 2.2 On va ajouter de volumes
On va ajouter trois volumes pour notre installation Airflow :
- data : c'est là que nous allons télécharger nos données
- models : là où on va stocker les modèles entraînés
- metrics : pour stocker nos résultats
Pour cela, nous allons ajouter après de la ligne 76 les lignes suivantes :
```
- ${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/data
- ${AIRFLOW_PROJ_DIR:-.}/models:/opt/airflow/models
- ${AIRFLOW_PROJ_DIR:-.}/metrics:/opt/airflow/metrics
```
Prêt ? Qu'est-ce que nous dit git ?
Allez, on push. Ça marche ?
## 3. Et Docker ?
C'est bien de modifier le docker-compose.yml, mais comment on met en route les conteneurs ?
Il faut installer docker.
Va sur [comment installer docker ?](https://docs.docker.com/get-docker/) et suit les instructions pour ta machine.
Une fois l'installation finie, lance un conteneur de test :
```bash
docker run hello-world
```
Tu auras une sortie similaire à celle-ci :
```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
c1ec31eb5944: Pull complete 
Digest: sha256:4bd78111b6914a99dbc560e6a20eab57ff6655aea4a80c50b0c5491968cbc2e6
Status: Downloaded newer image for hello-world:latest
  
Hello from Docker!
This message shows that your installation appears to be working correctly.
  
To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```
### 3.1 On lance la configuration d'airflow
Au même niveau que le fichier docker-compose.yml, exécute 
```
docker compose up airflow-init
```
Cela va configurer la base de données et créer les utilisateurs d'Airflow. Par défaut airflow/airflow.
### 3.2 On lance airflow
Une fois que l'init est fini, on peut lancer le reste :
```bash
docker compose up
```
Attends un peu, ensuite tu peux aller sur [localhost:8080](http://localhost:8080) sur l'interface Airflow.
Si tu veux regarder un peu le code tu aller [ici](http://localhost:8080/dags/tutorial/grid?tab=code) (il faut être connecté localement)

