from __future__ import annotations
from google.cloud.firestore_v1.field_path import FieldPath


def range_by_id(db, collection, doc_id) -> list:
    client = db.collection(collection)
    filter1 = db.document(f'{collection}/{doc_id}')
    filter2 = db.document(f'{collection}/{doc_id}_z')
    return client.where(FieldPath.document_id(), u'>=', filter1).where(FieldPath.document_id(), '<', filter2).get()


def get_by_id(db, collection, doc_id) -> list:
    client = db.collection(collection)
    filter1 = db.document(f'{collection}/{doc_id}')
    return client.where(FieldPath.document_id(), u'==', filter1).get()


def get_by(db, collection, field_name, field_value) -> list:
    client = db.collection(collection)
    return client.where(field_name, u'==', field_value).get()


def update(db, collection, document, obj):
    doc_ref = db.collection(collection).document(document)
    doc_ref.update(obj)


def add(db, collection, document, obj):
    doc_ref = db.collection(collection).document(document)
    doc_ref.set(obj)


def get_all(db, collection):
    client = db.collection(collection)
    return client.get()
