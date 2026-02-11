# Backend (Meeting Room Agent API)

FastAPI + LangGraph. PostgreSQL 연동, 회의실 예약/조회 에이전트.

- **실행**: `uvicorn server:app --host 0.0.0.0 --port 8000`
- **엔드포인트**: `GET /health`, `POST /run` (body: `{"query": "..."}`)
- **설정**: 상위 디렉터리 또는 `backend/` 에 `.env` (OPENAI_API_KEY, DB_*)
