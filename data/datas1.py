from pymongo import MongoClient
import requests


def fetch_and_insert_data(db, collection_name, url, limit=100):
    collection = db[collection_name]
    offset = 0

    while True:
        payload = {'limit': limit, 'offset': offset}
        response = requests.get(url, params=payload)

        if response.status_code == 200:
            data = response.json()
            collection.insert_many(data['results'])
            if len(data['results']) < limit:
                break
            else:
                offset += limit


# Provide the connection details
hostname = 'localhost'
port = 27017  # Default MongoDB port

# Create a MongoClient instance
client = MongoClient(hostname, port)

db = client['projetSNCF']  # projetSNCF = database de notre projet

# Example usage for sncf23 collection
url23 = 'https://data.sncf.com/api/explore/v2.1/catalog/datasets/incidents-de-securite-epsf/records'
fetch_and_insert_data(db, "sncf23", url23)

# Example usage for sncf1522 collection
url1522 = 'https://data.sncf.com/api/explore/v2.1/catalog/datasets/incidents-securite/records'
fetch_and_insert_data(db, "sncf1522", url1522)

# Example usage for sncfLigneE collection
urlLigneE = 'https://data.sncf.com/api/explore/v2.1/catalog/datasets/liste-des-lignes-electrifiees/records'
fetch_and_insert_data(db, "sncfLigneE", urlLigneE)

# Example usage for sncf_l_admin collection
url_l_admin = 'https://data.sncf.com/api/explore/v2.1/catalog/datasets/lignes-par-region-administrative/records'
fetch_and_insert_data(db, "sncf_l_admin", url_l_admin)

# Example usage for sncfLigneT collection
urlLigneT = 'https://data.sncf.com/api/explore/v2.1/catalog/datasets/lignes-par-type/records'
fetch_and_insert_data(db, "sncfLigneT", urlLigneT)
