import logging
import upswingutil as ul
from firebase_admin import firestore, get_app, storage


class Firestore:
    org_collection = 'Organizations'
    sub_collection_properties = 'properties'
    credentials = 'credentials'

    def __init__(self, app=None):
        self.firestore_db = firestore.client(app=get_app(app)) if app else firestore.client()
        self.firestore_storage = storage.bucket(name=f'{ul.G_CLOUD_PROJECT}.appspot.com', app=get_app(app)) if app else storage.bucket(name=f'{ul.G_CLOUD_PROJECT}.appspot.com')

    def get_collection(self, name):
        return self.firestore_db.collection(name)

    def get_collection_docs(self, name):
        return self.firestore_db.collection(name).stream()

    def get_ref_collection(self, name):
        return self.firestore_db.collection(name)

    def get_ref_document(self, name, doc):
        return self.firestore_db.collection(name).document(doc).get()

    def write_doc(self, collection: str, doc: str, data: dict):
        __ref__ = self.firestore_db.collection(collection).document(doc)
        __ref__.set(data, merge=True)
        logging.debug(f"Document written successfully")

    def update_doc(self, collection: str, doc: str, data: dict):
        __ref__ = self.firestore_db.collection(collection).document(doc)
        __ref__.update(data)
        logging.debug(f"Document Updated successfully")

    def increment_doc_value(self, collection: str, doc: str, data: str, incr: int):
        __ref__ = self.firestore_db.collection(collection).document(doc)
        __ref__.update({
            data: firestore.firestore.Increment(incr)
        })

    def upload_document_firestorage(self, folder: str, imgData):
        blob_ref = self.firestore_storage.blob(folder)
        logging.debug(f"Blob Reference -> {blob_ref}")
        blob_ref.upload_from_string(imgData)
        # logging.debug(blob_ref.public_url)
        return blob_ref.public_url
