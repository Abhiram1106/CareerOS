# NEXUS ATS Service

This service is implemented directly from the ATS folder blueprint files:
- `next_gen_ats_design_blueprint.html`
- `NEXUS_ATS_Blueprint.docx`

## Implemented API groups (v1)
- Requisitions API
- Candidates API
- Applications API
- Interviews API
- Scorecards API
- Offers API
- AI Intelligence API (match, parse, enhancement, prediction, bias-scan, rediscovery, chat)
- Webhook event catalog API

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8010
```

Health: `GET /health`

OpenAPI docs: `http://localhost:8010/docs`
