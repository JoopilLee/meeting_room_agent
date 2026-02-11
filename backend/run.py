import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import app.core.config  # noqa: F401
from app.core.config import check_env_set
from app.db.session import init_db
from app.graph.workflow import get_agent


def run(query: str) -> dict:
    ok, missing = check_env_set()
    if not ok:
        raise RuntimeError(f"필수 환경 변수가 없습니다: {missing}. .env에 OPENAI_API_KEY를 설정하세요.")
    init_db()
    agent = get_agent()
    return agent.invoke({"query": query})


if __name__ == "__main__":
    default_query = "에펠탑 17층 1702-A 2025-08-13 10:00~11:00 비었어?"
    user_query = sys.argv[1] if len(sys.argv) > 1 else default_query
    result = run(user_query)
    print(result.get("final_answer", ""))
