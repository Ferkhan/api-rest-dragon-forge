import firebase_admin
from firebase_admin import credentials, firestore, db

class FirebaseDB:
    def __init__(self, cred_path, db_url):
        # Initialize the Firebase Admin SDK with account credentials
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': db_url
        })
        # self.db = firestore.client()
        # self.realtime_db = db.reference('/')

    # def get_firestore_data(self, collection_name):
    #     # Get data from Firestore
    #     collection_ref = self.db.collection(collection_name)
    #     docs = collection_ref.stream()
    #     return {doc.id: doc.to_dict() for doc in docs}

    # def get_realtime_db_data(self, path):
    #     # Get data from Realtime Database
    #     return self.realtime_db.child(path).get()
    
    def write_record(self, path, data):
        # Write a record to Realtime Database
        ref = db.reference(path)
        ref.set(data)
    
    def read_record(self, path):
        # Read a record from Realtime Database
        ref = db.reference(path)
        return ref.get()
    
    def update_record(self, path, data):
        # Update a record in Realtime Database
        ref = db.reference(path)
        ref.update(data)

    def delete_record(self, path):
        # Delete a record from Realtime Database
        ref = db.reference(path)
        ref.delete()