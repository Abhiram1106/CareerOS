from app.modules.rewrite.dto.proof_rewrite_dto import ProofRewriteRequest
from app.modules.rewrite.mutation.proof_linked_rewrite_handler import ProofLinkedRewriteHandler


def test_rewrite_schema_and_unsupported_metrics():
    payload = ProofRewriteRequest(
        resume_json={
            "sections": [
                {
                    "section_name": "experience",
                    "content_json": {"raw": "Led team of 5 engineers and improved throughput by 40%"},
                }
            ]
        },
        jd_json={"skills": {"required": ["Python"]}},
        evidence_json={"claims": []},
        ats_flags=["two_column_layout"],
    )
    result = ProofLinkedRewriteHandler().execute(payload)
    assert result["section_rewrites"]
    assert result["unsupported_claims"]
    assert result["top_issues"][0]["type"] == "ATS_FORMAT"
