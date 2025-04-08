from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "EduTrack"

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[DATABASE_NAME]

response = client.admin.command('ping')

if response.get("ok") == 1.0:
    print("Connected to database!")
else:
    print("Connection is failed!")

trainers_collection = db["trainers"]
subjects_collection = db["subjects"]
admin_collection = db["admin"] 


admin_exists = admin_collection.find_one({'username': 'admin'})

if admin_exists:
    print("Admin already Created!")
else:
    hashed_password = generate_password_hash("admin")  
    admin_collection.insert_one({
        "username": "admin",
        "password": hashed_password
    })
    print("admin created with default username & password.")