# meeting_room_agent — 별도 Git 저장소로 올리기

이 프로젝트는 `repository/meeting_room_agent`에 복사된 상태입니다.  
아래 순서대로 하면 GitHub에 **별도 repository**로 등록할 수 있습니다.

## 1. 새 Git 저장소 초기화

```bash
cd /Users/a11609/Desktop/repository/meeting_room_agent
git init
git add .
git commit -m "Initial commit: meeting_room_agent (LangGraph + PostgreSQL + Docker)"
```

## 2. GitHub에서 새 저장소 생성

1. GitHub → **New repository**
2. Repository name: `meeting_room_agent` (또는 원하는 이름)
3. **Create repository** (README, .gitignore 추가하지 않음)

## 3. 원격 연결 후 푸시

GitHub에서 안내한 URL을 사용합니다. 예: `https://github.com/YOUR_USERNAME/meeting_room_agent.git`

```bash
git remote add origin https://github.com/YOUR_USERNAME/meeting_room_agent.git
git branch -M main
git push -u origin main
```

## 4. (선택) LLM_AGENT에서 제거

별도 레포로 잘 올라갔다면, 예전 위치의 폴더는 삭제해도 됩니다.

```bash
rm -rf /Users/a11609/Desktop/repository/LLM_AGENT/meeting_room_agent
```

이후 LLM_AGENT의 `README.md`에서 meeting_room_agent 설명을 제거하거나,  
“별도 저장소로 이전됨: https://github.com/…” 로 수정해 두면 됩니다.
