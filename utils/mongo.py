import pymongo

client = pymongo.MongoClient("mongodb+srv://andrewedwardrobinson:MongoDB@cluster0.4zdcdya.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client['breeze_bot']


general = db["pterodactyl"]
