# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import sqlite3
import base64
from pathlib import Path
import os
from datetime import datetime
from passlib.context import CryptContext

# ====================== CONFIGURATION ======================
class Config:
    def __init__(self):
        self.BASE_DIR = Path(__file__).parent
        self.STATIC_DIR = self.BASE_DIR / "static"
        self.DATABASE = str(self.BASE_DIR / "aeerck.db")
        
        # Identité AEERCK
        self.ORG_NAME = "Amicale des Élèves et Étudiants Ressortissants de la Commune de Kounkané"
        self.ORG_ACRONYM = "A.E.E.R.C.K"
        self.SLOGAN = "L'union notre vertu, l'excellence notre credo"
        self.COLORS = {
            "primary": "#000000",  # Noir
            "secondary": "#FFFFFF", # Blanc
            "accent": "#008000"    # Vert
        }
        
        # Encodage du logo
        logo_path = self.STATIC_DIR / "images" / "logo.png"
        self.LOGO_BASE64 = None
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                self.LOGO_BASE64 = base64.b64encode(f.read()).decode('utf-8')

config = Config()

# ====================== APPLICATION ======================
app = FastAPI(
    title=config.ORG_ACRONYM,
    description=f"Plateforme officielle de {config.ORG_NAME}",
    version="1.0.0"
)

# ====================== BASE DE DONNÉES ======================
def get_db():
    db = sqlite3.connect(config.DATABASE)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialisation simplifiée et sécurisée de la base"""
    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
    
    with sqlite3.connect(config.DATABASE) as conn:
        cursor = conn.cursor()
        
        # Table Membres
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id TEXT UNIQUE,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password_hash TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            is_admin BOOLEAN DEFAULT 0
        )
        """)
        
        # Compte admin par défaut
        try:
            cursor.execute(
                "INSERT INTO members (member_id, first_name, last_name, email, password_hash, is_admin) VALUES (?, ?, ?, ?, ?, ?)",
                ("ADMIN001", "Admin", "System", "admin@aeerck.org", pwd_context.hash("admin123"), 1)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            pass

# ====================== ROUTES ======================
@app.on_event("startup")
async def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{config.ORG_ACRONYM}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            :root {{
                --primary: {config.COLORS['primary']};
                --secondary: {config.COLORS['secondary']};
                --accent: {config.COLORS['accent']};
            }}
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: var(--secondary);
                color: var(--primary);
            }}
            .header {{
                background: var(--primary);
                color: white;
                padding: 1rem;
                text-align: center;
            }}
            .logo {{
                max-width: 150px;
                height: auto;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <img src="data:image/png;base64,{config.LOGO_BASE64}" alt="Logo" class="logo">
            <h1>{config.ORG_NAME}</h1>
            <p><em>{config.SLOGAN}</em></p>
        </div>
    </body>
    </html>
    """

@app.get("/api/info")
async def api_info():
    return {
        "organisation": config.ORG_NAME,
        "sigle": config.ORG_ACRONYM,
        "slogan": config.SLOGAN,
        "couleurs": config.COLORS
    }

# ====================== FICHIERS STATIQUES ======================
app.mount("/static", StaticFiles(directory=config.STATIC_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)