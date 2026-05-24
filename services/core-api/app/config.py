import os
from pathlib import Path

def _default_benchmark_path() -> Path:
    """Monorepo root in dev; shallow /app layout in Docker (file may be absent)."""
    here = Path(__file__).resolve()
    if len(here.parents) > 3:
        return here.parents[3] / "docs" / "benchmarks" / "benchmark_runs.json"
    return Path("docs/benchmarks/benchmark_runs.json")


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./careeros_dev.db")
BENCHMARK_ARTIFACT_PATH = os.getenv(
    "BENCHMARK_ARTIFACT_PATH",
    str(_default_benchmark_path()),
)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
ATS_ENGINE_URL = os.getenv("ATS_ENGINE_URL", "http://localhost:8001")
AI_REWRITER_URL = os.getenv("AI_REWRITER_URL", "http://localhost:8003")
RESUME_PARSER_URL = os.getenv("RESUME_PARSER_URL", "http://localhost:8004")
MATCH_ENGINE_URL = os.getenv("MATCH_ENGINE_URL", "http://localhost:8005")
JOBS_FEED_URL = os.getenv("JOBS_FEED_URL", "http://localhost:8006")
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "30"))
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALG = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_BASE = os.getenv("LLM_API_BASE", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
AUTO_CREATE_TABLES = os.getenv("AUTO_CREATE_TABLES", "false").lower() == "true"
EXPORTS_DIR = os.getenv("EXPORTS_DIR", "./exports")
EXPORT_STORAGE = os.getenv("EXPORT_STORAGE", "local").lower()
S3_EXPORT_BUCKET = os.getenv("S3_EXPORT_BUCKET", "")
S3_EXPORT_PREFIX = os.getenv("S3_EXPORT_PREFIX", "resume-exports")
S3_REGION = os.getenv("S3_REGION", "ap-south-1")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "")
EXPORT_SIGNED_URL_TTL_SECONDS = int(os.getenv("EXPORT_SIGNED_URL_TTL_SECONDS", "900"))

_weasy_env = os.getenv("WEASYPRINT_ENABLED", "auto").lower()
if _weasy_env == "auto":
    WEASYPRINT_ENABLED = os.name != "nt"
else:
    WEASYPRINT_ENABLED = _weasy_env == "true"
