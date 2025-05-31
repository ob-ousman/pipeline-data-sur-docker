# Tester la connexion
docker version

# Tester avec une commande simple
docker run hello-world

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
