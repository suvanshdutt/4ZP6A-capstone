from pymongo import MongoClient

# MongoDB Atlas credentials
MONGO_URI = "mongodb+srv://chestxraygrpacc:y40YFGS0bNGSPHSY@chestxray.qfyks.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)

# Get all database names
databases = client.list_database_names()

# System databases that should not be deleted
protected_databases = {"admin", "local", "config"}

# Delete all non-system databases
for db_name in databases:
    if db_name not in protected_databases:
        client.drop_database(db_name)
        print(f"❌ Dropped database: {db_name}")

# Close connection
client.close()
print("🔌 Connection closed.")