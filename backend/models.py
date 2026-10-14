from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.db import Base
def utcnow(): return datetime.utcnow()
class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    mrr: Mapped[float] = mapped_column(Float, default=0.0)
    days_since_login: Mapped[int] = mapped_column(Integer, default=0)
    tickets_open: Mapped[int] = mapped_column(Integer, default=0)
    nps: Mapped[float] = mapped_column(Float, default=7.0)
    risk: Mapped[float] = mapped_column(Float, default=0.0)
    band: Mapped[str] = mapped_column(String(32), default="low", index=True)
    playbook: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
