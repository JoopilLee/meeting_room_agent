import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

_root_app = Path(__file__).resolve().parent.parent.parent  # backend/
# Load .env from project root (meeting_room_agent/) then backend/ for overrides
for _env_path in (_root_app.parent / ".env", _root_app / ".env"):
    if _env_path.exists():
        load_dotenv(dotenv_path=_env_path)


def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")
    dbname = os.getenv("DB_NAME", "meeting_room")
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


_llm: Optional[ChatOpenAI] = None


def get_llm() -> ChatOpenAI:
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODEL", "gpt-4.1"),
            temperature=0.2,
            max_retries=2,
            max_tokens=None,
        )
    return _llm


def __getattr__(name: str):
    """Lazy-load llm to avoid OPENAI_API_KEY requirement when only DB config is needed (e.g. Alembic)."""
    if name == "llm":
        return get_llm()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def check_env_set() -> tuple:
    required = ["OPENAI_API_KEY"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        return False, ", ".join(missing)
    return True, ""


def check_db_configured() -> bool:
    if os.getenv("DATABASE_URL"):
        return True
    return bool(os.getenv("DB_HOST") or os.getenv("DB_USER") or os.getenv("DB_NAME"))
