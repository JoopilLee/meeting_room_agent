import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from run import run as agent_run

app = FastAPI(title="Meeting Room Agent", description="회의실 예약/조회 LangGraph 에이전트 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    query: str


class RunResponse(BaseModel):
    final_answer: str
    success: bool = True


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run", response_model=RunResponse)
def run_agent(req: RunRequest):
    try:
        result = agent_run(req.query)
        answer = result.get("final_answer", "")
        return RunResponse(final_answer=answer, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
