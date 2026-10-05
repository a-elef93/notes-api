# Notes API

A small REST API for storing and reading notes, built with **Flask** and **Redis** and run with **Docker Compose**.

The goal of this project is to practice multi-container setups and data persistence: notes are stored in Redis, which uses a named Docker volume, so the data survives `docker compose down` and `up`.

## Stack

- Python 3.11 / Flask
- Redis (`redis:alpine`)
- Docker & Docker Compose

## Run it

```bash
git clone git@github.com:a-elef93/notes-api.git
cd notes-api
docker compose up -d --build
```

The API is available at `http://localhost:5000`.

## Endpoints

| Method | Path     | Description          |
|--------|----------|----------------------|
| POST   | /notes   | Add a note           |
| GET    | /notes   | List all notes       |

```bash
curl -X POST localhost:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"text": "first note"}'

curl localhost:5000/notes
```

## Data persistence

Redis stores its data in the named volume `redis_data`, mounted at `/data`.
Notes survive container removal:

```bash
docker compose down
docker compose up -d
curl localhost:5000/notes   # notes are still there
```

Note: `docker compose down -v` also removes the volume and deletes the data.

## Project structure

```
.
├── app.py               # Flask application
├── requirements.txt     # Python dependencies
├── Dockerfile           # Image for the web service
└── docker-compose.yml   # web + redis services, named volume
```

## Configuration

| Variable     | Default | Description                  |
|--------------|---------|------------------------------|
| `REDIS_HOST` | `redis` | Hostname of the Redis service |
