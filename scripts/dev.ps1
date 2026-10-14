# Dev server for churn-risk-console
$env:LLM_MODE = "mock"
uvicorn backend.main:app --reload --port 8000
