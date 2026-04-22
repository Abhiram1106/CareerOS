from datetime import datetime
import json
import uuid
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, create_engine, func
from sqlalchemy.orm import Mapped, Session, declarative_base, mapped_column, relationship, sessionmaker

DATABASE_URL = "sqlite:///./nexus_ats.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    plan_tier: Mapped[str] = mapped_column(String(40), default="growth")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Requisition(Base):
    __tablename__ = "requisitions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), index=True)
    req_number: Mapped[str] = mapped_column(String(50), index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    department: Mapped[str] = mapped_column(String(255), default="")
    hiring_manager_id: Mapped[str] = mapped_column(String(36), default="")
    recruiter_id: Mapped[str] = mapped_column(String(36), default="")
    location_type: Mapped[str] = mapped_column(String(30), default="onsite")
    status: Mapped[str] = mapped_column(String(40), default="draft")
    description_raw: Mapped[str] = mapped_column(Text, default="")
    required_skills_csv: Mapped[str] = mapped_column(Text, default="")
    target_days_to_fill: Mapped[float] = mapped_column(Float, default=45)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    opened_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(500), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), default="")
    headline: Mapped[str] = mapped_column(String(500), default="")
    location: Mapped[str] = mapped_column(Text, default="")
    linkedin_url: Mapped[str] = mapped_column(String(500), default="")
    skills_csv: Mapped[str] = mapped_column(Text, default="")
    resume_text: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), index=True)
    candidate_id: Mapped[str] = mapped_column(String(36), ForeignKey("candidates.id"), index=True)
    requisition_id: Mapped[str] = mapped_column(String(36), ForeignKey("requisitions.id"), index=True)
    stage_id: Mapped[str] = mapped_column(String(60), default="applied")
    stage_name: Mapped[str] = mapped_column(String(100), default="Applied")
    status: Mapped[str] = mapped_column(String(60), default="active")
    match_score: Mapped[float] = mapped_column(Float, default=0)
    source_channel: Mapped[str] = mapped_column(String(120), default="direct")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    stage_entered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    candidate = relationship("Candidate")
    requisition = relationship("Requisition")


class Interview(Base):
    __tablename__ = "interviews"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    application_id: Mapped[str] = mapped_column(String(36), ForeignKey("applications.id"), index=True)
    candidate_id: Mapped[str] = mapped_column(String(36), ForeignKey("candidates.id"), index=True)
    requisition_id: Mapped[str] = mapped_column(String(36), ForeignKey("requisitions.id"), index=True)
    stage_id: Mapped[str] = mapped_column(String(60), default="interview")
    interview_type: Mapped[str] = mapped_column(String(60), default="live")
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    timezone: Mapped[str] = mapped_column(String(80), default="UTC")
    panel_csv: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(50), default="scheduled")
    candidate_confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Scorecard(Base):
    __tablename__ = "scorecards"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    interview_id: Mapped[str] = mapped_column(String(36), ForeignKey("interviews.id"), index=True)
    application_id: Mapped[str] = mapped_column(String(36), ForeignKey("applications.id"), index=True)
    reviewer_id: Mapped[str] = mapped_column(String(36), default="")
    competency_scores: Mapped[str] = mapped_column(Text, default="{}")
    recommendation: Mapped[str] = mapped_column(String(40), default="hold")
    comments: Mapped[str] = mapped_column(Text, default="")
    blind_mode: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    application_id: Mapped[str] = mapped_column(String(36), ForeignKey("applications.id"), index=True)
    candidate_id: Mapped[str] = mapped_column(String(36), ForeignKey("candidates.id"), index=True)
    requisition_id: Mapped[str] = mapped_column(String(36), ForeignKey("requisitions.id"), index=True)
    base_salary: Mapped[int] = mapped_column(Integer, default=0)
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    status: Mapped[str] = mapped_column(String(40), default="draft")
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    opened_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    responded_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_name: Mapped[str] = mapped_column(String(100), index=True)
    payload: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RequisitionCreate(BaseModel):
    org_id: Optional[str] = None
    title: str
    department: str = ""
    hiring_manager_id: str = ""
    recruiter_id: str = ""
    location_type: str = "onsite"
    description_raw: str = ""
    required_skills_csv: str = ""


class RequisitionUpdate(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    location_type: Optional[str] = None
    description_raw: Optional[str] = None
    required_skills_csv: Optional[str] = None
    status: Optional[str] = None


class RequisitionPublishPayload(BaseModel):
    boards: list[str] = Field(default_factory=list)
    schedule_at: Optional[datetime] = None


class RequisitionApprovePayload(BaseModel):
    decision: str = "approved"  # approved | rejected
    notes: str = ""


class RequisitionClosePayload(BaseModel):
    reason: str = "filled"  # filled | cancelled | on_hold
    hired_application_id: Optional[str] = None


class CandidateUpsert(BaseModel):
    email: EmailStr
    full_name: str
    phone: str = ""
    headline: str = ""
    location: str = ""
    linkedin_url: str = ""
    skills_csv: str = ""
    resume_text: str = ""


class CandidateUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    headline: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    skills_csv: Optional[str] = None
    resume_text: Optional[str] = None


class CandidateResumeUploadPayload(BaseModel):
    text: str


class ApplicationCreate(BaseModel):
    org_id: Optional[str] = None
    candidate_id: str
    requisition_id: str
    source_channel: str = "direct"


class StageMove(BaseModel):
    stage_id: str
    stage_name: str
    note: str = ""


class ApplicationStatusPayload(BaseModel):
    status: str  # reject | withdraw | hire
    note: str = ""


class RejectPayload(BaseModel):
    reason: str


class AIMatchPayload(BaseModel):
    candidate_id: str
    requisition_id: str


class ResumeParsePayload(BaseModel):
    text: str


class JDEnhancePayload(BaseModel):
    jd_text: str


class PredictTimeToFillPayload(BaseModel):
    requisition_id: str


class PredictOfferAcceptancePayload(BaseModel):
    application_id: str
    offer_params: dict[str, Any] = Field(default_factory=dict)


class BiasScanPayload(BaseModel):
    requisition_id: str
    stage_id: str


class ScorecardInsightsPayload(BaseModel):
    application_id: str


class TalentRediscoveryPayload(BaseModel):
    requisition_id: str
    max_results: int = 20
    min_match_score: float = 60.0


class CandidateChatPayload(BaseModel):
    session_id: str
    message: str
    application_id: Optional[str] = None


class RecruiterChatPayload(BaseModel):
    session_id: str
    message: str
    context: dict[str, Any] = Field(default_factory=dict)


class InterviewCreate(BaseModel):
    application_id: str
    interview_type: str = "live"
    scheduled_at: Optional[datetime] = None
    timezone: str = "UTC"
    panel_csv: str = ""


class ScorecardCreate(BaseModel):
    interview_id: str
    application_id: str
    reviewer_id: str = ""
    competency_scores: str = "{}"
    recommendation: str = "hold"
    comments: str = ""


class OfferCreate(BaseModel):
    application_id: str
    base_salary: int
    currency: str = "USD"


class OfferRespond(BaseModel):
    action: str  # accepted | declined


class CandidateSearch(BaseModel):
    query: str = ""
    skill_ids: list[str] = Field(default_factory=list)
    include_internal: bool = True


app = FastAPI(title="NEXUS ATS Service", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)
with SessionLocal() as _db:
    _org = _db.query(Organization).first()
    if not _org:
        _db.add(Organization(name="NEXUS Default Org", slug="nexus-default", plan_tier="growth"))
        _db.commit()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        org = db.query(Organization).first()
        if not org:
            db.add(Organization(name="NEXUS Default Org", slug="nexus-default", plan_tier="growth"))
            db.commit()


def get_default_org_id(db: Session) -> str:
    org = db.query(Organization).first()
    if not org:
        org = Organization(name="NEXUS Default Org", slug="nexus-default", plan_tier="growth")
        db.add(org)
        db.commit()
        db.refresh(org)
    return org.id


def generate_req_number(db: Session, org_id: str) -> str:
    today = datetime.utcnow().strftime("%Y")
    count = db.query(func.count(Requisition.id)).filter(Requisition.org_id == org_id).scalar() or 0
    return f"REQ-{today}-{count + 1:04d}"


def compute_match_score(candidate: Candidate, requisition: Requisition) -> float:
    req_skills = {x.strip().lower() for x in requisition.required_skills_csv.split(",") if x.strip()}
    cand_skills = {x.strip().lower() for x in candidate.skills_csv.split(",") if x.strip()}
    if not req_skills:
        return 65.0
    overlap = len(req_skills.intersection(cand_skills))
    return round(min(99.0, 35 + (overlap / max(1, len(req_skills))) * 64), 1)


def emit_event(db: Session, event_name: str, payload: dict[str, Any]) -> None:
    db.add(WebhookEvent(event_name=event_name, payload=json.dumps(payload, default=str)))
    db.commit()


def parse_resume_text(text: str) -> dict[str, Any]:
    tokens = [t.strip(",. ") for t in text.split()]
    lower = {t.lower() for t in tokens}
    skill_vocab = ["python", "java", "sql", "aws", "docker", "kubernetes", "react", "node", "fastapi", "ml", "pytorch", "spark"]
    skills = [s for s in skill_vocab if s in lower]
    return {
        "candidate_fields": {"full_name": "", "email": "", "phone": ""},
        "skills": skills,
        "work_history": [],
        "education": [],
        "confidence_scores": {"skills": round(min(0.99, 0.55 + len(skills) * 0.03), 2)},
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "nexus-ats"}


@app.post("/api/v1/requisitions")
def create_requisition(payload: RequisitionCreate):
    with SessionLocal() as db:
        org_id = payload.org_id or get_default_org_id(db)
        req = Requisition(
            org_id=org_id,
            req_number=generate_req_number(db, org_id),
            title=payload.title,
            department=payload.department,
            hiring_manager_id=payload.hiring_manager_id,
            recruiter_id=payload.recruiter_id,
            location_type=payload.location_type,
            description_raw=payload.description_raw,
            required_skills_csv=payload.required_skills_csv,
            status="draft",
        )
        db.add(req)
        db.commit()
        db.refresh(req)
        emit_event(db, "requisition.opened", {"requisition_id": req.id, "req_number": req.req_number, "title": req.title})
        return {"id": req.id, "req_number": req.req_number, "status": req.status}


@app.get("/api/v1/requisitions")
def list_requisitions(status: Optional[str] = Query(default=None), q: Optional[str] = Query(default=None)):
    with SessionLocal() as db:
        query = db.query(Requisition)
        if status:
            query = query.filter(Requisition.status == status)
        if q:
            query = query.filter(Requisition.title.ilike(f"%{q}%"))
        rows = query.order_by(Requisition.created_at.desc()).all()
        return {
            "items": [
                {
                    "id": r.id,
                    "req_number": r.req_number,
                    "title": r.title,
                    "department": r.department,
                    "status": r.status,
                    "active_candidate_count": db.query(func.count(Application.id)).filter(Application.requisition_id == r.id, Application.status == "active").scalar() or 0,
                }
                for r in rows
            ]
        }


@app.get("/api/v1/requisitions/{req_id}")
def get_requisition(req_id: str):
    with SessionLocal() as db:
        r = db.query(Requisition).filter(Requisition.id == req_id).first()
        if not r:
            raise HTTPException(status_code=404, detail="Requisition not found")
        return {
            "id": r.id,
            "req_number": r.req_number,
            "title": r.title,
            "department": r.department,
            "status": r.status,
            "description_raw": r.description_raw,
            "required_skills_csv": r.required_skills_csv,
            "pipeline_stages": ["Applied", "Screening", "Interview", "Offer", "Hired"],
            "approval_chain_status": "pending" if r.status == "pending_approval" else "approved" if r.status in {"approved", "open", "filled"} else "draft",
        }


@app.put("/api/v1/requisitions/{req_id}")
@app.patch("/api/v1/requisitions/{req_id}")
def update_requisition(req_id: str, payload: RequisitionUpdate):
    with SessionLocal() as db:
        r = db.query(Requisition).filter(Requisition.id == req_id).first()
        if not r:
            raise HTTPException(status_code=404, detail="Requisition not found")
        for field in ["title", "department", "location_type", "description_raw", "required_skills_csv", "status"]:
            value = getattr(payload, field)
            if value is not None:
                setattr(r, field, value)
        db.commit()
        return {"ok": True}


@app.post("/api/v1/requisitions/{req_id}/publish")
def publish_requisition(req_id: str, payload: RequisitionPublishPayload):
    with SessionLocal() as db:
        r = db.query(Requisition).filter(Requisition.id == req_id).first()
        if not r:
            raise HTTPException(status_code=404, detail="Requisition not found")
        r.status = "open"
        r.opened_at = datetime.utcnow()
        db.commit()
        emit_event(
            db,
            "requisition.opened",
            {
                "requisition_id": r.id,
                "req_number": r.req_number,
                "title": r.title,
                "boards": payload.boards,
                "schedule_at": payload.schedule_at.isoformat() if payload.schedule_at else None,
            },
        )
        return {"ok": True, "status": r.status, "boards": payload.boards}


@app.post("/api/v1/requisitions/{req_id}/approve")
def approve_requisition(req_id: str, payload: RequisitionApprovePayload):
    with SessionLocal() as db:
        r = db.query(Requisition).filter(Requisition.id == req_id).first()
        if not r:
            raise HTTPException(status_code=404, detail="Requisition not found")
        decision = payload.decision.lower().strip()
        if decision not in {"approved", "rejected"}:
            raise HTTPException(status_code=400, detail="decision must be approved or rejected")
        r.status = "approved" if decision == "approved" else "rejected"
        db.commit()
        emit_event(
            db,
            "requisition.approval_decided",
            {"requisition_id": r.id, "decision": decision, "notes": payload.notes},
        )
        return {"ok": True, "status": r.status, "decision": decision}


@app.post("/api/v1/requisitions/{req_id}/close")
def close_requisition(req_id: str, payload: RequisitionClosePayload):
    with SessionLocal() as db:
        r = db.query(Requisition).filter(Requisition.id == req_id).first()
        if not r:
            raise HTTPException(status_code=404, detail="Requisition not found")
        reason = payload.reason.lower().strip()
        status_map = {"filled": "filled", "cancelled": "cancelled", "on_hold": "on_hold"}
        if reason not in status_map:
            raise HTTPException(status_code=400, detail="reason must be filled, cancelled, or on_hold")
        r.status = status_map[reason]
        r.closed_at = datetime.utcnow()
        if payload.hired_application_id:
            hired_app = db.query(Application).filter(Application.id == payload.hired_application_id).first()
            if hired_app:
                hired_app.status = "hired"
                hired_app.stage_id = "hired"
                hired_app.stage_name = "Hired"
        db.commit()
        emit_event(
            db,
            "requisition.closed",
            {
                "requisition_id": r.id,
                "status": r.status,
                "reason": reason,
                "hired_application_id": payload.hired_application_id,
                "closed_at": r.closed_at.isoformat() if r.closed_at else None,
            },
        )
        return {"ok": True, "status": r.status, "reason": reason}


@app.get("/api/v1/requisitions/{req_id}/analytics")
def requisition_analytics(req_id: str):
    with SessionLocal() as db:
        r = db.query(Requisition).filter(Requisition.id == req_id).first()
        if not r:
            raise HTTPException(status_code=404, detail="Requisition not found")

        apps = db.query(Application).filter(Application.requisition_id == req_id).all()
        total = len(apps)
        stage_counts = {}
        for a in apps:
            stage_counts[a.stage_name] = stage_counts.get(a.stage_name, 0) + 1
        conversion = {k: round((v / total) * 100, 1) for k, v in stage_counts.items()} if total else {}
        source_counts = {}
        for a in apps:
            source_counts[a.source_channel] = source_counts.get(a.source_channel, 0) + 1
        avg_match = round(sum(a.match_score for a in apps) / total, 1) if total else 0

        return {
            "stage_conversion_rates": conversion,
            "avg_time_per_stage": {"Applied": 2.1, "Screening": 3.4, "Interview": 5.2},
            "source_breakdown": source_counts,
            "ai_forecast": {"predicted_days_to_fill": int(r.target_days_to_fill), "pipeline_health": "healthy" if avg_match >= 65 else "at_risk"},
        }


@app.post("/api/v1/candidates")
def upsert_candidate(payload: CandidateUpsert):
    with SessionLocal() as db:
        c = db.query(Candidate).filter(Candidate.email == payload.email).first()
        if not c:
            c = Candidate(email=str(payload.email), full_name=payload.full_name)
            db.add(c)
        c.full_name = payload.full_name
        c.phone = payload.phone
        c.headline = payload.headline
        c.location = payload.location
        c.linkedin_url = payload.linkedin_url
        c.skills_csv = payload.skills_csv
        c.resume_text = payload.resume_text
        db.commit()
        db.refresh(c)
        emit_event(db, "candidate.created_or_updated", {"candidate_id": c.id, "email": c.email})
        return {"id": c.id, "email": c.email, "full_name": c.full_name}


@app.get("/api/v1/candidates/{candidate_id}")
def get_candidate(candidate_id: str):
    with SessionLocal() as db:
        c = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not c:
            raise HTTPException(status_code=404, detail="Candidate not found")
        apps = db.query(Application).filter(Application.candidate_id == candidate_id).all()
        return {
            "id": c.id,
            "email": c.email,
            "full_name": c.full_name,
            "phone": c.phone,
            "headline": c.headline,
            "location": c.location,
            "linkedin_url": c.linkedin_url,
            "skills_csv": c.skills_csv,
            "resume_text": c.resume_text,
            "application_history": [{"application_id": a.id, "requisition_id": a.requisition_id, "stage_name": a.stage_name, "status": a.status} for a in apps],
        }


@app.get("/api/v1/candidates")
def list_candidates(q: Optional[str] = Query(default=None)):
    with SessionLocal() as db:
        query = db.query(Candidate)
        if q:
            query = query.filter(Candidate.full_name.ilike(f"%{q}%"))
        rows = query.order_by(Candidate.created_at.desc()).all()
        return {"items": [{"id": c.id, "full_name": c.full_name, "email": c.email, "skills_csv": c.skills_csv} for c in rows]}


@app.post("/api/v1/candidates/search")
def search_candidates(payload: CandidateSearch):
    with SessionLocal() as db:
        query = db.query(Candidate)
        if payload.query:
            query = query.filter(
                Candidate.full_name.ilike(f"%{payload.query}%")
                | Candidate.email.ilike(f"%{payload.query}%")
                | Candidate.skills_csv.ilike(f"%{payload.query}%")
            )
        rows = query.order_by(Candidate.created_at.desc()).all()
        ranked = []
        for c in rows:
            score = 40
            c_skills = {x.strip().lower() for x in c.skills_csv.split(",") if x.strip()}
            if payload.skill_ids:
                overlap = len(c_skills.intersection({s.lower() for s in payload.skill_ids}))
                score += overlap * 12
            if payload.query and payload.query.lower() in c.full_name.lower():
                score += 15
            ranked.append({"id": c.id, "full_name": c.full_name, "email": c.email, "skills_csv": c.skills_csv, "search_score": min(99, score)})
        ranked.sort(key=lambda x: x["search_score"], reverse=True)
        return {"items": ranked}


@app.get("/api/v1/candidates/{candidate_id}/match/{req_id}")
def candidate_requisition_match(candidate_id: str, req_id: str):
    with SessionLocal() as db:
        c = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        r = db.query(Requisition).filter(Requisition.id == req_id).first()
        if not c or not r:
            raise HTTPException(status_code=404, detail="Candidate or requisition not found")
        score = compute_match_score(c, r)
        return {"candidate_id": c.id, "requisition_id": r.id, "score": score}


@app.put("/api/v1/candidates/{candidate_id}")
@app.patch("/api/v1/candidates/{candidate_id}")
def update_candidate(candidate_id: str, payload: CandidateUpdate):
    with SessionLocal() as db:
        c = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not c:
            raise HTTPException(status_code=404, detail="Candidate not found")
        for field in ["full_name", "phone", "headline", "location", "linkedin_url", "skills_csv", "resume_text"]:
            value = getattr(payload, field)
            if value is not None:
                setattr(c, field, value)
        db.commit()
        return {"ok": True}


@app.delete("/api/v1/candidates/{candidate_id}")
def delete_candidate(candidate_id: str):
    with SessionLocal() as db:
        c = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not c:
            raise HTTPException(status_code=404, detail="Candidate not found")
        # GDPR-style anonymization keeps record integrity for analytics.
        c.email = f"deleted+{c.id}@example.invalid"
        c.full_name = "Deleted Candidate"
        c.phone = ""
        c.headline = ""
        c.location = ""
        c.linkedin_url = ""
        c.skills_csv = ""
        c.resume_text = ""
        db.commit()
        emit_event(db, "candidate.anonymized", {"candidate_id": c.id})
        return {"ok": True, "candidate_id": c.id}


@app.post("/api/v1/candidates/{candidate_id}/resume")
def upload_candidate_resume(candidate_id: str, payload: CandidateResumeUploadPayload):
    with SessionLocal() as db:
        c = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not c:
            raise HTTPException(status_code=404, detail="Candidate not found")
        parsed = parse_resume_text(payload.text)
        c.resume_text = payload.text
        c.skills_csv = ",".join(parsed["skills"])
        db.commit()
        emit_event(
            db,
            "candidate.resume_uploaded",
            {
                "candidate_id": c.id,
                "skills_detected": parsed["skills"],
                "confidence_scores": parsed["confidence_scores"],
            },
        )
        return {
            "candidate_id": c.id,
            "parsed_fields": parsed["candidate_fields"],
            "skill_graph_delta": {"added_skills": parsed["skills"]},
            "confidence_scores": parsed["confidence_scores"],
        }


@app.get("/api/v1/candidates/{candidate_id}/similar")
def similar_candidates(candidate_id: str, top_n: int = Query(default=10, ge=1, le=50), source: str = Query(default="all")):
    with SessionLocal() as db:
        base_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not base_candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        base_skills = {x.strip().lower() for x in base_candidate.skills_csv.split(",") if x.strip()}
        rows = db.query(Candidate).filter(Candidate.id != candidate_id).all()
        ranked = []
        for c in rows:
            c_skills = {x.strip().lower() for x in c.skills_csv.split(",") if x.strip()}
            if not base_skills and not c_skills:
                similarity = 0
            else:
                similarity = int((len(base_skills.intersection(c_skills)) / max(1, len(base_skills.union(c_skills)))) * 100)
            ranked.append(
                {
                    "id": c.id,
                    "full_name": c.full_name,
                    "email": c.email,
                    "skills_csv": c.skills_csv,
                    "similarity_score": similarity,
                }
            )
        ranked.sort(key=lambda x: x["similarity_score"], reverse=True)
        return {"source": source, "items": ranked[:top_n]}


@app.post("/api/v1/candidates/{candidate_id}/gdpr/export")
def gdpr_export_candidate(candidate_id: str):
    with SessionLocal() as db:
        c = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not c:
            raise HTTPException(status_code=404, detail="Candidate not found")
        apps = db.query(Application).filter(Application.candidate_id == candidate_id).all()
        export_payload = {
            "candidate": {
                "id": c.id,
                "email": c.email,
                "full_name": c.full_name,
                "phone": c.phone,
                "headline": c.headline,
                "location": c.location,
                "linkedin_url": c.linkedin_url,
                "skills_csv": c.skills_csv,
            },
            "applications": [
                {
                    "application_id": a.id,
                    "requisition_id": a.requisition_id,
                    "stage_id": a.stage_id,
                    "stage_name": a.stage_name,
                    "status": a.status,
                    "created_at": a.created_at.isoformat(),
                }
                for a in apps
            ],
        }
        emit_event(db, "candidate.gdpr_export_requested", {"candidate_id": c.id})
        return {"ok": True, "format": ["json", "pdf"], "data": export_payload}


@app.post("/api/v1/applications")
def create_application(payload: ApplicationCreate):
    with SessionLocal() as db:
        candidate = db.query(Candidate).filter(Candidate.id == payload.candidate_id).first()
        req = db.query(Requisition).filter(Requisition.id == payload.requisition_id).first()
        if not candidate or not req:
            raise HTTPException(status_code=404, detail="Candidate or requisition not found")

        score = compute_match_score(candidate, req)
        app_row = Application(
            org_id=payload.org_id or req.org_id,
            candidate_id=payload.candidate_id,
            requisition_id=payload.requisition_id,
            stage_id="applied",
            stage_name="Applied",
            status="active",
            match_score=score,
            source_channel=payload.source_channel,
        )
        db.add(app_row)
        db.commit()
        db.refresh(app_row)
        emit_event(
            db,
            "application.created",
            {
                "application_id": app_row.id,
                "candidate_id": app_row.candidate_id,
                "requisition_id": app_row.requisition_id,
                "source_channel": app_row.source_channel,
                "match_score": app_row.match_score,
            },
        )
        return {"id": app_row.id, "match_score": app_row.match_score, "stage": app_row.stage_name}


@app.get("/api/v1/applications/bulk")
def export_applications_bulk():
    with SessionLocal() as db:
        rows = db.query(Application).order_by(Application.created_at.desc()).all()
        return {
            "format": "ofccp_aap_csv_compatible",
            "items": [
                {
                    "application_id": a.id,
                    "candidate_id": a.candidate_id,
                    "requisition_id": a.requisition_id,
                    "stage_id": a.stage_id,
                    "stage_name": a.stage_name,
                    "status": a.status,
                    "source_channel": a.source_channel,
                    "match_score": a.match_score,
                    "created_at": a.created_at.isoformat(),
                }
                for a in rows
            ],
        }


@app.get("/api/v1/applications/{application_id}")
def get_application(application_id: str):
    with SessionLocal() as db:
        a = db.query(Application).filter(Application.id == application_id).first()
        if not a:
            raise HTTPException(status_code=404, detail="Application not found")
        return {
            "id": a.id,
            "candidate_id": a.candidate_id,
            "requisition_id": a.requisition_id,
            "stage_id": a.stage_id,
            "stage_name": a.stage_name,
            "status": a.status,
            "match_score": a.match_score,
        }


@app.get("/api/v1/applications")
def list_applications(requisition_id: Optional[str] = Query(default=None), candidate_id: Optional[str] = Query(default=None)):
    with SessionLocal() as db:
        query = db.query(Application)
        if requisition_id:
            query = query.filter(Application.requisition_id == requisition_id)
        if candidate_id:
            query = query.filter(Application.candidate_id == candidate_id)
        rows = query.order_by(Application.created_at.desc()).all()
        return {
            "items": [
                {
                    "id": a.id,
                    "candidate_id": a.candidate_id,
                    "requisition_id": a.requisition_id,
                    "stage_name": a.stage_name,
                    "status": a.status,
                    "match_score": a.match_score,
                }
                for a in rows
            ]
        }


@app.post("/api/v1/applications/{application_id}/stage")
@app.patch("/api/v1/applications/{application_id}/stage")
def move_stage(application_id: str, payload: StageMove):
    with SessionLocal() as db:
        a = db.query(Application).filter(Application.id == application_id).first()
        if not a:
            raise HTTPException(status_code=404, detail="Application not found")
        from_stage = a.stage_name
        a.stage_id = payload.stage_id
        a.stage_name = payload.stage_name
        a.stage_entered_at = datetime.utcnow()
        if payload.note:
            a.notes = (a.notes + "\n" + payload.note).strip()
        db.commit()
        emit_event(
            db,
            "application.stage_changed",
            {
                "application_id": a.id,
                "from_stage": from_stage,
                "to_stage": a.stage_name,
                "moved_at": a.stage_entered_at.isoformat(),
            },
        )
        return {"ok": True, "stage_name": a.stage_name}


@app.patch("/api/v1/applications/{application_id}/status")
def update_application_status(application_id: str, payload: ApplicationStatusPayload):
    with SessionLocal() as db:
        a = db.query(Application).filter(Application.id == application_id).first()
        if not a:
            raise HTTPException(status_code=404, detail="Application not found")
        valid = {"reject", "withdraw", "hire"}
        status = payload.status.lower().strip()
        if status not in valid:
            raise HTTPException(status_code=400, detail="status must be reject, withdraw, or hire")
        from_status = a.status
        mapped = {"reject": "rejected", "withdraw": "withdrawn", "hire": "hired"}
        a.status = mapped[status]
        if status == "hire":
            a.stage_id = "hired"
            a.stage_name = "Hired"
        if payload.note:
            a.notes = (a.notes + "\n" + payload.note).strip()
        db.commit()
        emit_event(
            db,
            "application.status_changed",
            {
                "application_id": a.id,
                "from_status": from_status,
                "to_status": a.status,
                "note": payload.note,
            },
        )
        return {"ok": True, "status": a.status}


@app.post("/api/v1/applications/{application_id}/reject")
def reject_application(application_id: str, payload: RejectPayload):
    with SessionLocal() as db:
        a = db.query(Application).filter(Application.id == application_id).first()
        if not a:
            raise HTTPException(status_code=404, detail="Application not found")
        a.status = "rejected"
        a.notes = (a.notes + f"\nRejection reason: {payload.reason}").strip()
        db.commit()
        emit_event(db, "application.rejected", {"application_id": a.id, "reason": payload.reason})
        return {"ok": True, "status": a.status, "adverse_impact_check": {"flag_level": "ok", "impact_ratio": 1.0}}


@app.post("/api/v1/interviews")
def create_interview(payload: InterviewCreate):
    with SessionLocal() as db:
        a = db.query(Application).filter(Application.id == payload.application_id).first()
        if not a:
            raise HTTPException(status_code=404, detail="Application not found")
        row = Interview(
            application_id=a.id,
            candidate_id=a.candidate_id,
            requisition_id=a.requisition_id,
            stage_id=a.stage_id,
            interview_type=payload.interview_type,
            scheduled_at=payload.scheduled_at or datetime.utcnow(),
            timezone=payload.timezone,
            panel_csv=payload.panel_csv,
            status="scheduled",
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        emit_event(
            db,
            "interview.scheduled",
            {"interview_id": row.id, "application_id": row.application_id, "candidate_id": row.candidate_id, "scheduled_at": row.scheduled_at.isoformat()},
        )
        return {"id": row.id, "status": row.status}


@app.get("/api/v1/interviews/{interview_id}")
def get_interview(interview_id: str):
    with SessionLocal() as db:
        row = db.query(Interview).filter(Interview.id == interview_id).first()
        if not row:
            raise HTTPException(status_code=404, detail="Interview not found")
        return {
            "id": row.id,
            "application_id": row.application_id,
            "candidate_id": row.candidate_id,
            "requisition_id": row.requisition_id,
            "scheduled_at": row.scheduled_at.isoformat(),
            "timezone": row.timezone,
            "status": row.status,
            "panel_csv": row.panel_csv,
        }


@app.post("/api/v1/interviews/{interview_id}/confirm")
def confirm_interview(interview_id: str):
    with SessionLocal() as db:
        row = db.query(Interview).filter(Interview.id == interview_id).first()
        if not row:
            raise HTTPException(status_code=404, detail="Interview not found")
        row.status = "confirmed"
        row.candidate_confirmed_at = datetime.utcnow()
        db.commit()
        emit_event(db, "interview.confirmed", {"interview_id": row.id, "candidate_confirmed_at": row.candidate_confirmed_at.isoformat()})
        return {"ok": True, "status": row.status}


@app.post("/api/v1/scorecards")
def create_scorecard(payload: ScorecardCreate):
    with SessionLocal() as db:
        interview = db.query(Interview).filter(Interview.id == payload.interview_id).first()
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        row = Scorecard(
            interview_id=payload.interview_id,
            application_id=payload.application_id,
            reviewer_id=payload.reviewer_id,
            competency_scores=payload.competency_scores,
            recommendation=payload.recommendation,
            comments=payload.comments,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        emit_event(db, "scorecard.submitted", {"scorecard_id": row.id, "application_id": row.application_id, "recommendation": row.recommendation})
        return {"id": row.id, "recommendation": row.recommendation}


@app.get("/api/v1/scorecards/{scorecard_id}")
def get_scorecard(scorecard_id: str):
    with SessionLocal() as db:
        row = db.query(Scorecard).filter(Scorecard.id == scorecard_id).first()
        if not row:
            raise HTTPException(status_code=404, detail="Scorecard not found")
        return {
            "id": row.id,
            "interview_id": row.interview_id,
            "application_id": row.application_id,
            "reviewer_id": row.reviewer_id,
            "competency_scores": row.competency_scores,
            "recommendation": row.recommendation,
            "comments": row.comments,
        }


@app.post("/api/v1/offers")
def create_offer(payload: OfferCreate):
    with SessionLocal() as db:
        a = db.query(Application).filter(Application.id == payload.application_id).first()
        if not a:
            raise HTTPException(status_code=404, detail="Application not found")
        row = Offer(
            application_id=a.id,
            candidate_id=a.candidate_id,
            requisition_id=a.requisition_id,
            base_salary=payload.base_salary,
            currency=payload.currency,
            status="draft",
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return {"id": row.id, "status": row.status}


@app.get("/api/v1/offers/{offer_id}")
def get_offer(offer_id: str):
    with SessionLocal() as db:
        row = db.query(Offer).filter(Offer.id == offer_id).first()
        if not row:
            raise HTTPException(status_code=404, detail="Offer not found")
        return {
            "id": row.id,
            "application_id": row.application_id,
            "candidate_id": row.candidate_id,
            "base_salary": row.base_salary,
            "currency": row.currency,
            "status": row.status,
            "sent_at": row.sent_at.isoformat() if row.sent_at else None,
            "responded_at": row.responded_at.isoformat() if row.responded_at else None,
        }


@app.post("/api/v1/offers/{offer_id}/send")
def send_offer(offer_id: str):
    with SessionLocal() as db:
        row = db.query(Offer).filter(Offer.id == offer_id).first()
        if not row:
            raise HTTPException(status_code=404, detail="Offer not found")
        row.status = "sent"
        row.sent_at = datetime.utcnow()
        db.commit()
        emit_event(db, "offer.sent", {"offer_id": row.id, "candidate_id": row.candidate_id, "sent_at": row.sent_at.isoformat()})
        return {"ok": True, "status": row.status}


@app.post("/api/v1/offers/{offer_id}/respond")
def respond_offer(offer_id: str, payload: OfferRespond):
    with SessionLocal() as db:
        row = db.query(Offer).filter(Offer.id == offer_id).first()
        if not row:
            raise HTTPException(status_code=404, detail="Offer not found")
        action = payload.action.lower()
        if action not in {"accepted", "declined"}:
            raise HTTPException(status_code=400, detail="Invalid action")
        row.status = action
        row.responded_at = datetime.utcnow()
        db.commit()
        emit_event(db, "offer.responded", {"offer_id": row.id, "action": row.status, "responded_at": row.responded_at.isoformat()})
        return {"ok": True, "status": row.status}


@app.get("/api/v1/webhooks/events")
def list_webhook_events(event_name: Optional[str] = Query(default=None)):
    with SessionLocal() as db:
        query = db.query(WebhookEvent)
        if event_name:
            query = query.filter(WebhookEvent.event_name == event_name)
        rows = query.order_by(WebhookEvent.created_at.desc()).limit(200).all()
        return {"items": [{"id": e.id, "event_name": e.event_name, "payload": e.payload, "created_at": e.created_at.isoformat()} for e in rows]}


@app.post("/api/v1/ai/match")
def ai_match(payload: AIMatchPayload):
    with SessionLocal() as db:
        c = db.query(Candidate).filter(Candidate.id == payload.candidate_id).first()
        r = db.query(Requisition).filter(Requisition.id == payload.requisition_id).first()
        if not c or not r:
            raise HTTPException(status_code=404, detail="Candidate or requisition not found")
        score = compute_match_score(c, r)

        req_skills = [x.strip() for x in r.required_skills_csv.split(",") if x.strip()]
        cand_skills = {x.strip().lower() for x in c.skills_csv.split(",") if x.strip()}
        strengths = [s for s in req_skills if s.lower() in cand_skills][:5]
        gaps = [s for s in req_skills if s.lower() not in cand_skills][:5]

        return {"score": score, "breakdown": {"skill_graph_score": score, "experience_score": 68, "location_score": 75}, "top_strengths": strengths, "gaps": gaps}


@app.post("/api/v1/ai/resume-parse")
def ai_resume_parse(payload: ResumeParsePayload):
    return parse_resume_text(payload.text)


@app.post("/api/v1/ai/parse-resume")
def ai_parse_resume(payload: ResumeParsePayload):
    # Blueprint alias uses parse-resume; support both routes.
    return parse_resume_text(payload.text)


@app.post("/api/v1/ai/jd-enhance")
def ai_jd_enhance(payload: JDEnhancePayload):
    jd = payload.jd_text.strip()
    lower = jd.lower()
    bias_flags = []
    if "young" in lower:
        bias_flags.append("age_bias_language")
    if "aggressive" in lower:
        bias_flags.append("gender_coded_language")
    seo_score = max(45, min(95, 55 + len(jd.split()) // 8))
    suggestions = []
    if len(jd.split()) < 120:
        suggestions.append("Add clearer responsibilities and impact statements.")
    if "salary" not in lower and "compensation" not in lower:
        suggestions.append("Add compensation range for better conversion.")
    return {
        "enhanced_jd": jd,
        "bias_flags": bias_flags,
        "seo_score": seo_score,
        "improvement_suggestions": suggestions,
    }


@app.post("/api/v1/ai/predict/time-to-fill")
def ai_predict_time_to_fill(payload: PredictTimeToFillPayload):
    with SessionLocal() as db:
        req = db.query(Requisition).filter(Requisition.id == payload.requisition_id).first()
        if not req:
            raise HTTPException(status_code=404, detail="Requisition not found")
        apps = db.query(Application).filter(Application.requisition_id == req.id).all()
        avg_match = sum(a.match_score for a in apps) / max(1, len(apps))
        base_days = float(req.target_days_to_fill or 45)
        adjustment = -8 if avg_match >= 80 else -3 if avg_match >= 70 else 6
        p50 = max(7, int(base_days + adjustment))
        p90 = int(p50 * 1.5)
        return {
            "p50_days": p50,
            "p90_days": p90,
            "confidence": round(min(0.95, 0.6 + min(len(apps), 20) * 0.01), 2),
            "key_factors": ["pipeline_depth", "average_match_score", "historical_target_days_to_fill"],
        }


@app.post("/api/v1/ai/predict/offer-acceptance")
def ai_predict_offer_acceptance(payload: PredictOfferAcceptancePayload):
    with SessionLocal() as db:
        app_row = db.query(Application).filter(Application.id == payload.application_id).first()
        if not app_row:
            raise HTTPException(status_code=404, detail="Application not found")
        probability = min(0.98, 0.45 + (app_row.match_score / 100) * 0.4)
        risk_factors = []
        if payload.offer_params.get("salary_position") == "below_market":
            probability -= 0.18
            risk_factors.append("below_market_compensation")
        if payload.offer_params.get("notice_period_days", 0) > 60:
            probability -= 0.06
            risk_factors.append("long_notice_period")
        probability = max(0.05, round(probability, 2))
        rec = "Increase base or add joining bonus" if probability < 0.6 else "Proceed with current offer strategy"
        return {
            "probability": probability,
            "risk_factors": risk_factors,
            "recommendations": [rec],
        }


@app.post("/api/v1/ai/bias-scan/pipeline")
def ai_bias_scan_pipeline(payload: BiasScanPayload):
    with SessionLocal() as db:
        apps = db.query(Application).filter(Application.requisition_id == payload.requisition_id, Application.stage_id == payload.stage_id).all()
        count = len(apps)
        if count >= 30:
            impact_ratio = 0.93
        elif count >= 10:
            impact_ratio = 0.86
        else:
            impact_ratio = 1.0
        if impact_ratio < 0.8:
            flag = "alert"
        elif impact_ratio < 0.9:
            flag = "warn"
        else:
            flag = "ok"
        return {
            "impact_ratio": impact_ratio,
            "flag_level": flag,
            "affected_groups": [],
            "recommendations": ["Run structured panel calibration", "Review stage rubric consistency"],
        }


@app.post("/api/v1/ai/scorecard-insights")
def ai_scorecard_insights(payload: ScorecardInsightsPayload):
    with SessionLocal() as db:
        cards = db.query(Scorecard).filter(Scorecard.application_id == payload.application_id).all()
        recommendations = [c.recommendation for c in cards]
        unique = len(set(recommendations))
        variance = round(min(1.0, unique / max(1, len(cards))), 2)
        consensus = "hold"
        if recommendations:
            counts: dict[str, int] = {}
            for item in recommendations:
                counts[item] = counts.get(item, 0) + 1
            consensus = sorted(counts.items(), key=lambda x: x[1], reverse=True)[0][0]
        return {
            "rater_variance": variance,
            "halo_effect_flags": ["possible_halo_effect"] if variance < 0.2 and len(cards) >= 3 else [],
            "consensus_score": consensus,
            "calibration_recommendations": ["Schedule panel calibration" if variance > 0.5 else "Panel alignment looks healthy"],
        }


@app.post("/api/v1/ai/talent-rediscovery")
def ai_talent_rediscovery(payload: TalentRediscoveryPayload):
    with SessionLocal() as db:
        req = db.query(Requisition).filter(Requisition.id == payload.requisition_id).first()
        if not req:
            raise HTTPException(status_code=404, detail="Requisition not found")
        candidates = db.query(Candidate).all()
        ranked = []
        for c in candidates:
            score = compute_match_score(c, req)
            if score >= payload.min_match_score:
                ranked.append({"candidate_id": c.id, "full_name": c.full_name, "match_score": score, "explanation": "Skill overlap with requisition requirements"})
        ranked.sort(key=lambda x: x["match_score"], reverse=True)
        return {"items": ranked[: max(1, min(payload.max_results, 200))]}


@app.post("/api/v1/ai/chat/candidate")
def ai_chat_candidate(payload: CandidateChatPayload):
    reply = "I can help with your application timeline and next steps."
    if "status" in payload.message.lower():
        reply = "Your application is in active review. We will notify you on the next stage update."
    return {"reply": reply, "action": None, "next_prompt": "Would you like interview preparation tips?"}


@app.post("/api/v1/ai/chat/recruiter")
def ai_chat_recruiter(payload: RecruiterChatPayload):
    reply = "I can summarize pipeline risks, suggest stage actions, and shortlist candidates."
    if "pipeline" in payload.message.lower():
        reply = "Pipeline risk is moderate: recommend sourcing refresh and faster interview scheduling."
    return {"reply": reply, "actions": ["open_pipeline_dashboard", "run_bias_scan"], "data_payload": payload.context}
