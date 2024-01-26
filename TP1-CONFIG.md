# TP 1 - Configurer l'environnement 
## 1. Installer git
Si jamais, tu n'a pas git installé sur ta machine...
[Guide d'installation de git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)
Testes l'installation :
```bash
git --version
```
Tu dois avoir un message comme celui-ci : `git version 2.39.2 (Apple Git-143)` (selon la machine ça change...) mais en tout cas, pas une erreur.
## 2. Installer python 3.11
Nous allons utiliser la version 3.11 de python. 
## 3. Installer dvc
C'est mieux de créer un environnement virtuel pour que les choses restent propres :
#### Créer un dossier pour stocker l'environnement virtuel
```bash
mkdir ~/dvc-demo
python -m venv ~/dvc-demo
```
Après avoir exécutée la commande, le dossier `dvc-demo` doit contenir :
```bash
bin include lib pyvenv.cfg
```
Maintenant, il faut activer l'environnement :
```bash
source ~/dvc-demo/bin/activate
```
Dans la console, on doit voir quelque chose comme :
```
(dvc-demo) user@pc ~ %
```
Maintenant, on peut installer dvc (et les autres packages plus tard) dans notre environnement :
```bash
cd dvc-demo
pip install dvc
```
Vérifie l'installation de dvc :
```bash
dvc --version
```
C'est quoi la version installée de dvc ?
## 4. Installer docker
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
## 5. Clone le repo de travail
J'ai créé un repo sur Github avec certains éléments déjà prêts (et des choses qui ne nous intéressent pas).
Le repo contient une application web écrite en python avec FastAPI (très très simple). Cette application peut utiliser un modèle de machine learning depuis une interface web
1. Faites un fork sur ce repo : `https://github.com/juandavidcruzgomez/toy-web-service` sur ton Github
2. Clone le repo sur ta machine avec `git clone`
3. Explore un peu le code
## 6. Configure un environnement virtuel et lance le serveur

