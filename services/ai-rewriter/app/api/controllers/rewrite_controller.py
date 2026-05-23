from fastapi import APIRouter

from ...modules.rewrite.dto.proof_rewrite_dto import ProofRewriteRequest
from ...modules.rewrite.dto.resume_prompt_dto import ResumePrompt
from ...modules.rewrite.mutation.generate_resume_handler import GenerateResumeHandler
from ...modules.rewrite.mutation.proof_linked_rewrite_handler import ProofLinkedRewriteHandler

router = APIRouter()


@router.post("/generate/resume")
def generate_resume(payload: ResumePrompt):
    """Legacy template-fill generator — used by core-api resume generate until Week 4."""
    return GenerateResumeHandler().execute(payload)


@router.post("/rewrite")
def proof_linked_rewrite(payload: ProofRewriteRequest):
    """Proof-linked JSON-schema rewriter — no fabrication; unsupported_claims[] populated."""
    return ProofLinkedRewriteHandler().execute(payload)
