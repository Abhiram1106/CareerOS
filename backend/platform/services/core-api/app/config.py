import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./careeros_dev.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
ATS_ENGINE_URL = os.getenv("ATS_ENGINE_URL", "http://localhost:8001")
JOB_INTEL_URL = os.getenv("JOB_INTEL_URL", "http://localhost:8002")
AI_INFERENCE_URL = os.getenv("AI_INFERENCE_URL", "http://localhost:8003")
NEXUS_ATS_URL = os.getenv("NEXUS_ATS_URL", "http://localhost:8010")
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALG = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24
AUTO_CREATE_TABLES = os.getenv("AUTO_CREATE_TABLES", "false").lower() == "true"
EXPORTS_DIR = os.getenv("EXPORTS_DIR", "./exports")
EXPORT_STORAGE = os.getenv("EXPORT_STORAGE", "local").lower()
S3_EXPORT_BUCKET = os.getenv("S3_EXPORT_BUCKET", "")
S3_EXPORT_PREFIX = os.getenv("S3_EXPORT_PREFIX", "resume-exports")
S3_REGION = os.getenv("S3_REGION", "ap-south-1")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "")
EXPORT_SIGNED_URL_TTL_SECONDS = int(os.getenv("EXPORT_SIGNED_URL_TTL_SECONDS", "900"))

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", "")
RAZORPAY_CALLBACK_URL = os.getenv("RAZORPAY_CALLBACK_URL", "http://localhost:3000")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_SUCCESS_URL = os.getenv("STRIPE_SUCCESS_URL", "http://localhost:3000?checkout=success")
STRIPE_CANCEL_URL = os.getenv("STRIPE_CANCEL_URL", "http://localhost:3000?checkout=cancel")
ALERT_DISPATCH_INTERVAL_MINUTES = int(os.getenv("ALERT_DISPATCH_INTERVAL_MINUTES", "15"))

_weasy_env = os.getenv("WEASYPRINT_ENABLED", "auto").lower()
if _weasy_env == "auto":
    WEASYPRINT_ENABLED = os.name != "nt"
else:
    WEASYPRINT_ENABLED = _weasy_env == "true"
