import json
import os
from pathlib import Path

from flask import abort, jsonify, request
from pymongo import MongoClient, UpdateOne

from . import app

seed_songs = json.loads((Path(__file__).parent / "data" / "songs.json").read_text())
host = os.getenv("MONGODB_SERVICE", "localhost")
options = {"serverSelectionTimeoutMS": 5000}
if os.getenv("MONGODB_PORT"):
    options["port"] = int(os.environ["MONGODB_PORT"])
if os.getenv("MONGODB_USERNAME") and os.getenv("MONGODB_PASSWORD"):
    options["username"] = os.environ["MONGODB_USERNAME"]
    options["password"] = os.environ["MONGODB_PASSWORD"]
collection = MongoClient(host, **options).songs.songs


def seed_database():
    collection.create_index("id", unique=True)
    if collection.estimated_document_count() == 0:
        collection.bulk_write([
            UpdateOne({"id": song["id"]}, {"$setOnInsert": song}, upsert=True)
            for song in seed_songs
        ])


seed_database()


@app.get("/health")
def health():
    return jsonify(status="OK")


@app.get("/count")
def count():
    return jsonify(length=collection.count_documents({}))


@app.get("/song")
def get_songs():
    return jsonify(list(collection.find({}, {"_id": 0}).sort("id")))


@app.get("/song/<int:id>")
def get_song(id):
    song = collection.find_one({"id": id}, {"_id": 0})
    if song is None:
        abort(404)
    return jsonify(song)


@app.post("/song")
def create_song():
    from pymongo.errors import DuplicateKeyError

    song = request.get_json()
    if not isinstance(song, dict) or type(song.get("id")) is not int:
        abort(400)
    song = {key: value for key, value in song.items() if key != "_id"}
    try:
        collection.insert_one(song.copy())
    except DuplicateKeyError:
        abort(409)
    return jsonify(song), 201


@app.put("/song/<int:id>")
def update_song(id):
    song = request.get_json()
    if not isinstance(song, dict):
        abort(400)
    fields = {key: value for key, value in song.items() if key not in {"_id", "id"}}
    result = collection.update_one({"id": id}, {"$set": fields})
    if not result.matched_count:
        abort(404)
    return get_song(id)


@app.delete("/song/<int:id>")
def delete_song(id):
    if not collection.delete_one({"id": id}).deleted_count:
        abort(404)
    return "", 204
