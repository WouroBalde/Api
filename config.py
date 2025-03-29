import base64
from pathlib import Path

AEERCK_CONFIG = {
    "identity": {
        "name": "Amicale des Élèves et Étudiants...",
        "colors": {
            "primary": "#0055B7",
            "secondary": "#FFFFFF",
            "accent": "#F5A623"
        },
        "logo": base64.b64encode(Path("static/logo.png").read_bytes()).decode()
    },
    "fastapi_settings": {
        "title": "AEERCK Platform",
        "description": "Plateforme complète de gestion..."
    },
    "database": {
        "uri": "sqlite:///./aeerck.db"
    }
}