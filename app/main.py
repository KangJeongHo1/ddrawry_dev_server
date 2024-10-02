from fastapi import FastAPI, Request
from .models import *  # 모델을 임포트하여 테이블을 생성하도록 함
from fastapi.middleware.cors import CORSMiddleware



from .api.v1 import V1

app = FastAPI()
app.include_router(V1)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # 허용할 도메인
    allow_credentials=True,  # 쿠키 허용 여부
    allow_methods=["*"],  # 허용할 HTTP 메소드
    allow_headers=["*"],  # 허용할 헤더
)

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# 커스텀 에러 핸들러 (FastAPI 레벨에서 처리)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    missing_fields = [error['loc'][-1] for error in exc.errors()]
    message = f"다이어리를 작성하지 못했습니다. 필수 요소({', '.join(missing_fields)})가 누락되었습니다."
    return JSONResponse(
        status_code=400,
        content={
            "status": 400,
            "type": "error",
            "message": message
        },
    )

@app.get("/")
def read_root():
    return {"DDRAWRY": "This is ddrawry's API server"}
