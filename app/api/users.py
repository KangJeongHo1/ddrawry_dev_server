from fastapi import APIRouter, Request
from pydantic import BaseModel


router = APIRouter(prefix="/users")


# /users/settings
class Settings(BaseModel):
    dark_mode: bool | None = False
    notification: bool | None = False


current_settings = {
    "dark_mode": 0,
    "notification": 0
}

@router.patch("/settings")
async def settings(settings: Settings):
    message = None  # 초기 메시지 변수 설정

    # 다크 모드 설정 변경
    if "dark_mode" in settings.dict(exclude_unset=True):
        if settings.dark_mode not in [0, 1]:
            return {
                "status": 400,
                "message": "다크 모드는 0 또는 1로 설정해야 합니다."
            }
        current_settings["dark_mode"] = settings.dark_mode
        message = f"다크모드 변경 성공: {'true' if settings.dark_mode == 1 else 'false'}"  # 메시지에 현재 상태 추가

    # 알람 설정 변경
    if "notification" in settings.dict(exclude_unset=True):
        if settings.notification not in [0, 1]:
            return {
                "status": 400,
                "message": "알람 설정은 0 또는 1로 설정해야 합니다."
            }
        current_settings["notification"] = settings.notification
        message = f"알람 설정 변경 성공: {'true' if settings.notification == 1 else 'false'}"  # 메시지에 현재 상태 추가

    # 메시지가 설정되지 않은 경우
    if not message:
        return {
            "status": 200,
            "message": "설정이 변경되지 않았습니다."
        }

    return {
        "status": 200,
        "message": message  # 최종 메시지 반환
    }



# /users/nickname
@router.put("/nickname")
async def nickname(request: Request):
    json = await request.json()

    # request body가 없을 때 처리
    if not json:
        return {"status": 409, "message": "데이터가 없습니다."}

    nickname = json.get("nickname")
    
    # json에 nickname 필드가 없을 때 처리
    if not nickname:
        return {"status": 409, "message": "닉네임 데이터 없음", "request": json}

    # 닉네임 중복 확인
    if nickname in ["admin", "test"]:
        return {"status": 409, "message": "닉네임 중복"}
    
    # 닉네임 변경 성공 처리
    return {"status": 200, "message": "닉네임 변경 성공"}
