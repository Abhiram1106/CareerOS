from fastapi import APIRouter

from ...modules.rewrite.dto.proof_rewrite_dto import ProofRewriteRequest
from ...modules.rewrite.dto.resume_prompt_dto import ResumePrompt, ResumeStructuredPrompt
from ...modules.rewrite.mutation.generate_resume_handler import GenerateResumeHandler
from ...modules.rewrite.mutation.proof_linked_rewrite_handler import ProofLinkedRewriteHandler

router = APIRouter()


@router.post("/generate/resume")
def generate_resume(payload: ResumePrompt):
    """Legacy flat-field generator — backward compat."""
    # Wrap into the new structured format for compatibility
    from ...modules.rewrite.mutation.generate_resume_handler import _template_classic
    data = {
        "user": {"full_name": payload.full_name, "email": "", "phone": "", "linkedin_url": "", "github_url": "", "portfolio_url": ""},
        "profile": {"target_role": payload.target_role, "city": payload.city, "skills_csv": payload.skills_csv, "summary": payload.summary},
        "work_experiences": [],
        "educations": [],
        "skills": [],
        "projects": [],
        "certifications": [],
    }
    from ...modules.rewrite.dto.resume_prompt_dto import ResumeStructuredPrompt, ResumeGenerateResponse
    structured = ResumeStructuredPrompt(template_name=payload.template_name, profile_data=data)
    return GenerateResumeHandler().execute(structured)


@router.post("/generate/from-profile")
def generate_from_profile(payload: ResumeStructuredPrompt):
    """Generate resume from structured profile data (GET /profile/complete response)."""
    return GenerateResumeHandler().execute(payload)


@router.post("/rewrite")
def proof_linked_rewrite(payload: ProofRewriteRequest):
    """Proof-linked JSON-schema rewriter — no fabrication; unsupported_claims[] populated."""
    return ProofLinkedRewriteHandler().execute(payload)
