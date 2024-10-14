import datetime
import redis
from elasticsearch import Elasticsearch

# Connexion au serveur Redis
r = redis.Redis(host='localhost', port=6379, db=0)


# Connexion au serveur Elasticsearch

es = Elasticsearch([{'scheme': 'http', 'host': 'localhost', 'port': 9200}])


# Lire et stocker chaque ligne du fichier app_logs.txt dans Redis.
with open('app_logs.txt', 'r') as f:
    for line in f:
        # Séparation des différentes parties du log 
        parts = line.strip().split(" | ")
        timestamp = parts[0]
        log_type = parts[1]
        message = parts[2]
        details = parts[3] if len(parts) > 3 else ""

        # Générer un ID unique pour chaque log basé sur l'horodatage
        log_id = f"log:{int(datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').timestamp())}"

        # Stocker les informations dans un hash Redis
        r.hset(log_id, mapping={'timestamp': timestamp, 'type': log_type, 'message': message, 'details': details})
        print(f"Log {log_id} ajouté à Redis")
        
        
        
# Récupérer toutes les clés des logs
log_keys = r.keys('log:*')

# Afficher chaque log
for key in log_keys:
	log_data = r.hgetall(key)
	print(f"Log ID: {key.decode('utf-8')}")
	print(f"Timestamp: {log_data[b'timestamp'].decode('utf-8')}")
	print(f"Type: {log_data[b'type'].decode('utf-8')}")
	print(f"Message: {log_data[b'message'].decode('utf-8')}")
	print(f"Détails: {log_data[b'details'].decode('utf-8')}")
	print("-" * 40)
	
	
	
# Filtrer et afficher les logs d'erreur 
for key in log_keys:
    log_data = r.hgetall(key)
    # Vérifier si le type de log est "ERROR"
    if log_data[b'type'].decode('utf-8') == "ERROR":
        print(f"Log ID: {key.decode('utf-8')}")
        print(f"Message: {log_data[b'message'].decode('utf-8')}")
        print(f"Détails: {log_data[b'details'].decode('utf-8')}")
        print("-" * 40)


#Compter nb logs par type
for key in log_keys:
	log_data = r.hgetall(key)
	if log_data[b'type'].decode('utf-8') == "ERROR":
		# Définir une expiration de 3600 secondes (1 heure) r.expire(key, 3600)
		print(f"Log {key.decode('utf-8')} expirera dans 1 heure.")
		
log_count = {'INFO': 0, 'ERROR': 0, 'WARNING': 0}

for key in log_keys:
	log_data = r.hgetall(key)
	log_type = log_data[b'type'].decode('utf-8') 
	log_count[log_type] += 1
print("Nombre de logs par type :") 
print(log_count)





# Lire et stocker chaque ligne du fichier app_logs.txt dans Redis et Elasticsearch
with open('app_logs.txt', 'r') as f:
    for line in f:
        # Séparation des différentes parties du log
        parts = line.strip().split(" | ")
        timestamp = parts[0]
        log_type = parts[1]
        message = parts[2]
        details = parts[3] if len(parts) > 3 else ""

        # Générer un ID unique pour chaque log basé sur l'horodatage
        log_id = f"log:{int(datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').timestamp())}"

        # Stocker les informations dans un hash Redis
        r.hset(log_id, mapping={'timestamp': timestamp, 'type': log_type, 'message': message, 'details': details})

        # Stocker les informations dans Elasticsearch
        es.index(index='logs', id=log_id, body={
            'timestamp': timestamp,
            'type': log_type,
            'message': message,
            'details': details
        })

        print(f"Log {log_id} ajouté à Redis et Elasticsearch")
        
        
