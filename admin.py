from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from ..templates import admin
from .auth import admin_required

router = APIRouter()

@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(user=Depends(admin_required)):
    return admin.render_dashboard(
        title="Tableau de Bord AEERCK",
        sections=[
            {"name": "Membres", "url": "/admin/members"},
            {"name": "Événements", "url": "/admin/events"},
            {"name": "Votes", "url": "/admin/voting"}
        ]
    )