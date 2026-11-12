# Back-End-Development-Songs

Flask API for the Djirection song catalog. It uses MongoDB and seeds an empty catalog with the supplied sample songs.

Set `MONGODB_SERVICE` and, if needed, `MONGODB_PORT`, `MONGODB_USERNAME`, and `MONGODB_PASSWORD`. Run with `python -m flask --app app run --port 5001`, or build the included Dockerfile and serve port 8080.

The API supports `GET /health`, `GET /count`, `GET /song`, `POST /song`, and GET, PUT, and DELETE on `/song/<id>`. Run the starter health test with `python -m pytest` while MongoDB is reachable.
