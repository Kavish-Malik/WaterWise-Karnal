import firebase_admin
from firebase_admin import credentials, firestore

# Try with Key 1 or Key 2 JSON file
cred = credentials.Certificate("/Users/kavishmalik/Desktop/water/waterwise-karnal-1410-firebase-adminsdk-fbsvc-4e5e2d8a96.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

try:
    # Try reading a collection
    docs = db.collection("test").stream()
    for doc in docs:
        print(doc.id, doc.to_dict())
    print("✅ Connection successful")
except Exception as e:
    print("❌ Connection failed:", e)
