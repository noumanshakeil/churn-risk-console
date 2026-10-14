from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import churn as svc

class AccountIn(BaseModel):
    name: str = Field(min_length=2)
    mrr: float = 0
    days_since_login: int = 0
    tickets_open: int = 0
    nps: float = 7

router = APIRouter()

@router.get("/accounts")
async def accounts(db: AsyncSession = Depends(get_db)):
    rows = await svc.list_accounts(db)
    return {"accounts": [{"id": a.id, "name": a.name, "risk": a.risk, "band": a.band, "mrr": a.mrr, "playbook": a.playbook[:300]} for a in rows]}

@router.post("/accounts")
async def create(payload: AccountIn, db: AsyncSession = Depends(get_db)):
    a = await svc.upsert(db, payload.name, payload.mrr, payload.days_since_login, payload.tickets_open, payload.nps)
    return {"id": a.id, "risk": a.risk, "band": a.band}
