from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, HttpUrl

APP_DIR = Path(__file__).resolve().parent
DATA_FILE = Path(os.getenv("CATALOG_FILE", str(APP_DIR / "catalog.json")))

app = FastAPI(
    title="SLOOM AI COLLECTOR 365",
    description="Rights-aware metadata catalog for Asian films and series.",
    version="0.1.0",
)


class TitleIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    original_title: str | None = Field(default=None, max_length=200)
    country: str = Field(min_length=2, max_length=80)
    content_type: Literal["series", "film"]
    source_url: HttpUrl
    rights_holder: str | None = Field(default=None, max_length=200)
    license_status: Literal["unknown", "pending", "licensed", "rejected"] = "unknown"
    download_allowed: bool = False
    embed_allowed: bool = False
    territories: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    episode_count: int | None = Field(default=None, ge=1, le=1000)
    runtime_minutes: int | None = Field(default=None, ge=1, le=1000)
    arabic_subtitles: bool = False
    arabic_dubbing: bool = False
    nudity_review_status: Literal["not_reviewed", "passed", "failed"] = "not_reviewed"
    rights_evidence: str | None = Field(default=None, max_length=2000)


def load_records() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        raise HTTPException(status_code=500, detail="Catalog data file could not be read")


def save_records(records: list[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    temp_file = DATA_FILE.with_suffix(".tmp")
    temp_file.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    temp_file.replace(DATA_FILE)


@app.get("/")
def home():
    return {
        "name": "SLOOM AI COLLECTOR 365",
        "status": "running",
        "message": "Metadata catalog is ready. Video downloading is intentionally disabled.",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"ok": True, "service": "sloom-ai-collector-365"}


@app.get("/catalog")
def list_catalog():
    return load_records()


@app.post("/catalog", status_code=201)
def add_title(item: TitleIn):
    records = load_records()
    record = item.model_dump(mode="json")
    record["id"] = str(uuid4())
    record["approved_for_listing"] = False
    records.append(record)
    save_records(records)
    return record


@app.post("/catalog/{title_id}/approve")
def approve_title(title_id: str):
    records = load_records()
    for record in records:
        if record["id"] == title_id:
            if record["license_status"] != "licensed" or not record.get("rights_evidence"):
                raise HTTPException(
                    status_code=409,
                    detail="Cannot approve: verify a valid license and record its evidence first.",
                )
            record["approved_for_listing"] = True
            save_records(records)
            return record
    raise HTTPException(status_code=404, detail="Title not found")


@app.get("/catalog/{title_id}")
def get_title(title_id: str):
    for record in load_records():
        if record["id"] == title_id:
            return record
    raise HTTPException(status_code=404, detail="Title not found")
