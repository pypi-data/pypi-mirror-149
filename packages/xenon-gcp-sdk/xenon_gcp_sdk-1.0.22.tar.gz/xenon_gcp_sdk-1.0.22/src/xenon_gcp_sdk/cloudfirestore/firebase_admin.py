import firebase_admin
from firebase_admin import firestore


class FirebaseClient:

    def __init__(self):
        firebase_admin.initialize_app()
        self.db = firestore.client()
