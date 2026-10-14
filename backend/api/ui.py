from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import churn as svc

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Churn Risk Console", "accounts": await svc.list_accounts(db)})

@router.post("/ui/accounts")
async def ui_a(name: str = Form(...), mrr: float = Form(100), days_since_login: int = Form(14), tickets_open: int = Form(1), nps: float = Form(6), db: AsyncSession = Depends(get_db)):
    await svc.upsert(db, name, mrr, days_since_login, tickets_open, nps); return RedirectResponse("/", status_code=303)
