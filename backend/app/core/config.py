import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

_root_app = Path(__file__).resolve().parent.parent.parent
_env_path = _root_app / ".env"
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


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_MODEL", "gpt-4.1"),
        temperature=0.2,
        max_retries=2,
        max_tokens=None,
    )


llm = get_llm()


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
