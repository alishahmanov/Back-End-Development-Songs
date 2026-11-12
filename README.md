# Back-End-Development-Songs

Flask API for the Djirection song catalog. It uses MongoDB and seeds an empty catalog with the supplied sample songs.

Set `MONGODB_SERVICE` and, if needed, `MONGODB_PORT`, `MONGODB_USERNAME`, and `MONGODB_PASSWORD`. Run with `python -m flask --app app run --port 5001`, or build the included Dockerfile and serve port 8080.

The API supports `GET /health`, `GET /count`, `GET /song`, `POST /song`, and GET, PUT, and DELETE on `/song/<id>`. Run the starter health test with `python -m pytest` while MongoDB is reachable.

## Environment Setup

In IBM Skills Network Cloud IDE, use the lab MongoDB service, or run MongoDB locally and use `127.0.0.1`. The database is seeded automatically on first launch.

```sh
git clone https://github.com/alishahmanov/Back-End-Development-Songs.git
cd Back-End-Development-Songs
python3 -m venv .venv
source .venv/bin/activate
python -m pip install Flask pymongo pytest requests
export MONGODB_SERVICE=127.0.0.1
export MONGODB_PORT=27017
python -m flask --app app run --port 5000
```

Verify the API from another terminal with `curl -i http://127.0.0.1:5000/health` and `curl -i http://127.0.0.1:5000/song`. For OpenShift, set `MONGODB_SERVICE=mongo` on the Songs deployment and expose service port 8080.
