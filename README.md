# meeting_room_agent

회의실 예약/조회를 위한 LangGraph 기반 에이전트.  
빌딩·층·회의실 조회, 가용성 확인, 예약 생성·수정·취소, 내 예약 목록을 자연어로 처리합니다.

## 구조

- **backend/** — FastAPI + LangGraph (API: `/health`, `/run`)
- **frontend/** — Vite + React (회의실 에이전트 채팅 UI)
- **docker-compose** — db, backend, frontend 서비스 분리

## 설정

프로젝트 루트에 `.env`를 두고 다음 변수를 설정합니다.

| 변수 | 필수 | 설명 |
|------|------|------|
| `OPENAI_API_KEY` | O | OpenAI API 키 |
| `OPENAI_MODEL` | - | 기본값 `gpt-4.1` |
| `DB_HOST` | - | `localhost`|
| `DB_PORT` | - | `5432` |
| `DB_USER` | - | DB 사용자 |
| `DB_PASSWORD` | - | DB 비밀번호 |
| `DB_NAME` | - | DB 이름|

## 실행

### Docker (권장)

```bash
docker-compose up --build
```

- **DB**: `localhost:5432`
- **Backend API**: `http://localhost:8001` (health: `/health`, 에이전트: `POST /run`)
- **Frontend**: `http://localhost:3000` (브라우저에서 접속, `/api`는 backend로 프록시)

### 로컬 개발

**Backend**

```bash
cd backend
pip install -r requirements.txt
# .env는 프로젝트 루트 또는 backend/ 에 두고
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

브라우저에서 `http://localhost:5173` 접속. Vite가 `/api`를 `localhost:8000`으로 프록시합니다.

## 예시 쿼리

- `에펠탑 17층 1702-A 2025-08-13 10:00~11:00 비었어?` — 가용 여부
- `에펠탑 17층 1702-A 오늘 15:00~16:00 주간 회의 예약해줘. 주최자 홍길동` — 예약
- `예약 아이디 15473_1_1_20250813_1500 취소해줘` — 취소
- `홍길동 내 예약 보여줘` — 내 예약 목록
