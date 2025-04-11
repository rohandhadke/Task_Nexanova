# from pymongo import MongoClient
# from werkzeug.security import generate_password_hash

# MONGO_URI = "mongodb+srv://atlas-sample-dataset-load-67f94dabdfd5e55db92be973:<edu@#121>@edutrack.ytjm1ms.mongodb.net/?retryWrites=true&w=majority&appName=EduTrack"
# DATABASE_NAME = "EduTrack"

# client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
# db = client[DATABASE_NAME]

# response = client.admin.command('ping')

# if response.get("ok") == 1.0:
#     print("Connected to database!")
# else:
#     print("Connection is failed!")

# trainers_collection = db["trainers"]
# subjects_collection = db["subjects"]
# admin_collection = db["admin"] 


# admin_exists = admin_collection.find_one({'username': 'admin'})

# if admin_exists:
#     print("Admin already Created!")
# else:
#     hashed_password = generate_password_hash("admin")  
#     admin_collection.insert_one({
#         "username": "admin",
#         "password": hashed_password
#     })
#     print("admin created with default username & password.")


from pymongo import MongoClient
from urllib.parse import quote_plus
from werkzeug.security import generate_password_hash

username = quote_plus("user1")
password = quote_plus("password@user1")  # encode special characters

MONGO_URI = f"mongodb+srv://{username}:{password}@edutrack.ytjm1ms.mongodb.net/EduTrack"
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
