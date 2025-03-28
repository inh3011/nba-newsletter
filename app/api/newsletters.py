from fastapi import APIRouter, Response
from app.services.newsletter import render_newsletter_html

router = APIRouter()

@router.get("/preview")
def preview_newsletter():
    html = render_newsletter_html()
    return Response(content=html, media_type="text/html")