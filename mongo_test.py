from pymongo import MongoClient

uri = "mongodb+srv://ankit-suman:ankitsuman12345@cluster0.lvnpojz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

try:
    db = client["testdb"]
    db.test_collection.insert_one({"status": "working"})
    print("✅ MongoDB connection works!")
except Exception as e:
    print("❌ Error:", e)
