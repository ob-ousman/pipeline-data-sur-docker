# Vérifier que Docker est installé
docker --version

# Vérifier que Docker Compose est installé
docker-compose --version

# Vérifier que Docker est en cours d'exécution
docker info

# Vérifier la version de Docker
docker version

# Vérifier que Colima est installé
colima --version

# Vérifier que Colima est en cours d'exécution
colima status

# Lancer le deamon docker (MacOS)
colima start 

# Executer le projet
docker-compose up -d

# stopper le projet
docker-compose down

# Lister les conteneurs en cours d'exécution
docker ps

# se connecter à une image, exemple "zookeeper"
docker exec -it <nom_du_conteneur> /bin/sh
