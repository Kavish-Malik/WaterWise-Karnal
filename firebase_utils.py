import firebase_admin
from firebase_admin import credentials, firestore

# Initialize the app with your service account key file
cred = credentials.Certificate("/Users/kavishmalik/Desktop/water/waterwise-karnal-1410-firebase-adminsdk-fbsvc-4e5e2d8a96.json")
firebase_admin.initialize_app(cred)

# Create Firestore client
db = firestore.client()
