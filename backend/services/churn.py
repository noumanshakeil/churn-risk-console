from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.llm import get_llm
from backend.models import Account

def risk_score(days_since_login: int, tickets_open: int, nps: float) -> float:
    s = 0.1
    s += min(0.45, days_since_login / 60.0)
    s += min(0.3, tickets_open * 0.08)
    s += max(0.0, (7.0 - nps) * 0.05)
    return round(min(1.0, s), 3)

def band(score: float) -> str:
    if score >= 0.7: return "high"
    if score >= 0.4: return "medium"
    return "low"

async def upsert(session: AsyncSession, name: str, mrr: float, days_since_login: int, tickets_open: int, nps: float) -> Account:
    score = risk_score(days_since_login, tickets_open, nps)
    llm = get_llm()
    play = await llm.complete(
        f"Churn playbook for {name}: login_gap={days_since_login}, tickets={tickets_open}, nps={nps}, risk={score}",
        system="CSM coach. Give 3 concrete save actions.",
    )
    row = Account(id=uuid.uuid4().hex[:10], name=name[:160], mrr=float(mrr), days_since_login=int(days_since_login),
                  tickets_open=int(tickets_open), nps=float(nps), risk=score, band=band(score), playbook=play)
    session.add(row); await session.commit(); await session.refresh(row); return row

async def list_accounts(session: AsyncSession) -> list[Account]:
    return list((await session.execute(select(Account).order_by(Account.risk.desc()))).scalars())
