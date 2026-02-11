# Frontend (회의실 에이전트 UI)

Vite + React. Backend `/run` API 호출.

- **개발**: `npm install && npm run dev` → http://localhost:5173 (프록시: /api → backend:8000)
- **빌드**: `npm run build` → `dist/`
- **Docker**: nginx가 `dist` 서빙, `/api`는 backend로 프록시
