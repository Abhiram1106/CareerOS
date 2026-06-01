"""FastAPI dependency factories for handlers and query services (override in tests)."""

from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from .database import get_db
from .modules.agent.mutation.run_agent_handler import RunAgentHandler
from .modules.agent.query.agent_run_query_service import AgentRunQueryService
from .modules.assistant.mutation.chat_handler import ChatHandler
from .modules.ats.mutation.run_ats_scan_handler import RunATSParseSafetyHandler
from .modules.ats.query.ats_query_service import ATSQueryService
from .modules.auth.mutation.login_handler import LoginHandler
from .modules.auth.mutation.logout_handler import LogoutHandler
from .modules.auth.mutation.register_handler import RegisterHandler
from .modules.auth.mutation.reset_password_handler import (
    ConfirmPasswordResetHandler,
    RequestPasswordResetHandler,
)
from .modules.dashboard.query.dashboard_query_service import DashboardQueryService
from .modules.export.mutation.queue_export_handler import QueueExportHandler
from .modules.export.query.export_query_service import ExportQueryService
from .modules.jd.mutation.parse_jd_handler import ParseJDHandler
from .modules.profile.mutation.upsert_profile_handler import UpsertProfileHandler
from .modules.profile.query.profile_query_service import ProfileQueryService
from .modules.recommendation.mutation.run_rewrite_handler import RunRewriteHandler
from .modules.recommendation.query.recommendation_query_service import RecommendationQueryService
from .modules.resume.mutation.delete_resume_handler import DeleteResumeHandler
from .modules.resume.mutation.generate_resume_handler import GenerateResumeHandler
from .modules.resume.mutation.upload_resume_handler import UploadResumeHandler
from .modules.resume.query.resume_query_service import ResumeQueryService
from .modules.scorecard.mutation.score_resume_handler import ScoreResumeHandler


def get_register_handler(db: Session = Depends(get_db)) -> RegisterHandler:
    return RegisterHandler(db)


def get_login_handler(db: Session = Depends(get_db)) -> LoginHandler:
    return LoginHandler(db)


def get_logout_handler(db: Session = Depends(get_db)) -> LogoutHandler:
    return LogoutHandler(db)


def get_request_reset_handler(db: Session = Depends(get_db)) -> RequestPasswordResetHandler:
    return RequestPasswordResetHandler(db)


def get_confirm_reset_handler(db: Session = Depends(get_db)) -> ConfirmPasswordResetHandler:
    return ConfirmPasswordResetHandler(db)


def get_queue_export_handler(db: Session = Depends(get_db)) -> QueueExportHandler:
    return QueueExportHandler(db)


def get_export_query_service(db: Session = Depends(get_db)) -> ExportQueryService:
    return ExportQueryService(db)


def get_generate_resume_handler(db: Session = Depends(get_db)) -> GenerateResumeHandler:
    return GenerateResumeHandler(db)


def get_upload_resume_handler(db: Session = Depends(get_db)) -> UploadResumeHandler:
    return UploadResumeHandler(db)


def get_delete_resume_handler(db: Session = Depends(get_db)) -> DeleteResumeHandler:
    return DeleteResumeHandler(db)


def get_resume_query_service(db: Session = Depends(get_db)) -> ResumeQueryService:
    return ResumeQueryService(db)


def get_parse_jd_handler(db: Session = Depends(get_db)) -> ParseJDHandler:
    return ParseJDHandler(db)


def get_score_resume_handler(db: Session = Depends(get_db)) -> ScoreResumeHandler:
    return ScoreResumeHandler(db)


def get_run_rewrite_handler(db: Session = Depends(get_db)) -> RunRewriteHandler:
    return RunRewriteHandler(db)


def get_recommendation_query_service(db: Session = Depends(get_db)) -> RecommendationQueryService:
    return RecommendationQueryService(db)


def get_run_agent_handler(db: Session = Depends(get_db)) -> RunAgentHandler:
    return RunAgentHandler(db)


def get_agent_run_query_service(db: Session = Depends(get_db)) -> AgentRunQueryService:
    return AgentRunQueryService(db)


def get_ats_scan_handler(db: Session = Depends(get_db)) -> RunATSParseSafetyHandler:
    return RunATSParseSafetyHandler(db)


def get_ats_query_service(db: Session = Depends(get_db)) -> ATSQueryService:
    return ATSQueryService(db)


def get_profile_query_service(db: Session = Depends(get_db)) -> ProfileQueryService:
    return ProfileQueryService(db)


def get_upsert_profile_handler(db: Session = Depends(get_db)) -> UpsertProfileHandler:
    return UpsertProfileHandler(db)


def get_dashboard_query_service(db: Session = Depends(get_db)) -> DashboardQueryService:
    return DashboardQueryService(db)


def get_chat_handler(db: Session = Depends(get_db)) -> ChatHandler:
    return ChatHandler(db)
