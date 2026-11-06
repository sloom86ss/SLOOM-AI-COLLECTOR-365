# SLOOM AI COLLECTOR 365

A metadata-first catalog for Asian films and series intended for **SLOOM DRAMA 365**.

## Current starter scope
- Record titles, official source URLs, languages, episode counts and runtime.
- Track rights evidence and territory restrictions.
- Keep every title in review until a human approves its rights.
- Expose a small API for the catalog.

## Important rights rule
This starter **does not download, copy, proxy, or re-host video**. A public watch link or an embed option is not permission to download or commercially redistribute a title. Only add media downloading after obtaining written permission or a license that explicitly allows downloading, storage, and the intended territories/use.

## Run locally
```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open `/docs` for the API interface and `/health` for a health check.

## Render
Create a new **Web Service** from this repository:
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

The starter stores records in a local JSON file. Free hosting filesystems may be temporary; do not use this as permanent video storage or the only copy of your catalog.