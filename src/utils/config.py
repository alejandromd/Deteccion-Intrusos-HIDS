#!/usr/bin/env python3

from datetime import timedelta
from pathlib import Path

class Config():

    APP_DIR = Path(__file__).resolve().parent.parent.parent
    ART_DIR = APP_DIR / "src/static/claymore_art.txt"

    BATCH_SIZE = 100

    VAULT_DIR = 'vault'

    CHECK_INTERVAL = timedelta(days=1)

settings = Config()