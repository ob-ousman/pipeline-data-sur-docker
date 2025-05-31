**DEVELOPPEMENT D'UN PIPELINE DATA AVEC SPARK+KAFKA+MONGODB SUR UN ENVIRONEMENT DOCKER**

![Apperçu](image.png)

**1. Liste de pieces-jointes**
- docker-compose.yml
- pipeline.py
- producer.py
- repertoire data
- ce fichier Readme.md
- Le fichier cmd (un condensé des commandes docker)

**2. Guide d'installation**

1. Demarrer les services Dockers avec la commande
    ``colima start`` # spécific à MacOS

2. Demarrer les container docker avec la commande
    ``docker-compose up -d``

3. Creer le topic sur le container Kafka (si ce n'est pas déjà fait)
    - se connecter au contener ``docker exec -it kafka /bin/bash``
    - créer le topic ``kafka-topics --create --topic iot-topic --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1``

4. Copier le script du pipeline dans le container spark-master
    - Copie du fichier ``docker cp pipeline.py spark-master:/opt/bitnami/spark/``
    - Connexion au container : ``docker exec -it spark-master /bin/bash``

5. Executer le script avec Spark sur le container Spark
   ``spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.mongodb.spark:mongo-spark-connector_2.12:10.2.0 /opt/bitnami/spark/pipeline.py``

6. il faut creer un prodcuteur et faire le test sur le container Kafka
    - creer un productuer ``kafka-console-producer --topic iot-topic --bootstrap-server kafka:9092``
    - tester en envoyant un message ``{"sensor_id": "S123", "timestamp": "2025-05-30T14:30:00Z", "temperature": 55.0, "humidity": 65.2, "status": "normal", "location": "factory_A"}``

7. Vérifier si spark a intercepté le message et a sauvegardé les donnée dans mongoDB
  - Si tout s'est bien passé, plusieurs fichiers seront créé dans le repertoire "./data" de la machine local
  - En cas d'erreur, consulter le log du container kafka avec la commande ``docker logs mongodb``
  - En cas de probleme de droit, accorder les droits necessaire à kafka avec le commande ``sudo chown -R 999:999 ./data``. Il faut relancer le container par la suite

7. Maintent il faut automatiser le producteur et copier le fichier avec la commande ``docker cp producer.py kafka:/``
   - installer la lib kafka si ce n'eest pas ``python -m pip install kafka-python``
   - et demarrer le script avec ``python /producer.py``

