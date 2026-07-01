from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.auth import require_dashboard_auth
from app.db import get_db
from app.models import Lead, LeadRecommendation, Task, User

router = APIRouter(tags=["dashboard"], dependencies=[Depends(require_dashboard_auth)])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=48)
    stats = {
        "total_leads": db.scalar(select(func.count(Lead.id))) or 0,
        "active_leads": db.scalar(select(func.count(Lead.id)).where(Lead.status.notin_(["ganho", "perdido"]))) or 0,
        "hot_leads": db.scalar(select(func.count(Lead.id)).where(Lead.temperature == "quente")) or 0,
        "stalled_leads": db.scalar(select(func.count(Lead.id)).where(Lead.status.notin_(["ganho", "perdido"]), Lead.updated_at <= cutoff)) or 0,
        "open_tasks": db.scalar(select(func.count(Task.id)).where(Task.status == "aberta")) or 0,
        "won_leads": db.scalar(select(func.count(Lead.id)).where(Lead.status == "ganho")) or 0,
    }
    recent_leads = db.execute(select(Lead).order_by(Lead.updated_at.desc()).limit(8)).scalars().all()
    broker_rows = db.execute(
        select(User.name, func.count(Lead.id))
        .join(Lead, Lead.broker_id == User.id, isouter=True)
        .where(User.role == "broker")
        .group_by(User.name)
        .order_by(func.count(Lead.id).desc())
    ).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "stats": stats, "recent_leads": recent_leads, "broker_rows": broker_rows},
    )


@router.get("/leads", response_class=HTMLResponse)
def leads_page(request: Request, db: Session = Depends(get_db)):
    leads = db.execute(select(Lead).order_by(Lead.updated_at.desc()).limit(200)).scalars().all()
    return templates.TemplateResponse("leads.html", {"request": request, "leads": leads})


@router.get("/leads/{lead_id}", response_class=HTMLResponse)
def lead_detail_page(lead_id: int, request: Request, db: Session = Depends(get_db)):
    lead = db.get(Lead, lead_id)
    recommendations = []
    tasks = []
    if lead:
        recommendations = db.execute(
            select(LeadRecommendation).where(LeadRecommendation.lead_id == lead.id).order_by(LeadRecommendation.created_at.desc())
        ).scalars().all()
        tasks = db.execute(select(Task).where(Task.lead_id == lead.id).order_by(Task.created_at.desc())).scalars().all()
    return templates.TemplateResponse(
        "lead_detail.html",
        {"request": request, "lead": lead, "recommendations": recommendations, "tasks": tasks},
    )


@router.get("/corretores", response_class=HTMLResponse)
def brokers_page(request: Request, db: Session = Depends(get_db)):
    brokers = db.execute(select(User).where(User.role == "broker").order_by(User.name.asc())).scalars().all()
    rows = []
    for broker in brokers:
        active = db.scalar(select(func.count(Lead.id)).where(Lead.broker_id == broker.id, Lead.status.notin_(["ganho", "perdido"]))) or 0
        hot = db.scalar(select(func.count(Lead.id)).where(Lead.broker_id == broker.id, Lead.temperature == "quente")) or 0
        rows.append({"broker": broker, "active": active, "hot": hot})
    return templates.TemplateResponse("brokers.html", {"request": request, "rows": rows})
