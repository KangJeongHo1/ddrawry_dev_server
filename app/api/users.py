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
                "message": "다크 모드는 true 또는 false로 설정해야 합니다."
            }
        current_settings["dark_mode"] = settings.dark_mode
        message = "다크모드 설정이 성공적으로 업데이트 되었습니다."  # 메시지에 현재 상태 추가

        return {
            "status": 200,
            "message": message,
            "data": {
                "id": 1,
                "dark_mode": True if settings.dark_mode == 1 else False
            }
        }
    # 알람 설정 변경
    if "notification" in settings.dict(exclude_unset=True):
        if settings.notification not in [0, 1]:
            return {
                "status": 400,
                "message": "알람 설정은 true 또는 false로 설정해야 합니다."
            }
        current_settings["notification"] = settings.notification
        message = "알림 설정이 성공적으로 업데이트 되었습니다."  # 메시지에 현재 상태 추가

        return {
            "status": 200,
            "message": message,
            "data": {
                "id": 1,
                "notification": True if settings.notification == 1 else False
            }
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
    return {
        "status": 200, 
        "message": "닉네임 변경 성공",
        "data": {
            "id": 1,
            "nickname": nickname
        }
    }

# /users/profile
@router.get("/profile")
async def profile():
    
    dummy_data = {
        "id": 1,
        "nickname": "포카칩",
        "dark_mode": False,
        "notification": True
    }      

    return {
        "status": 200, 
        "message": "1번 유저 조회 완료",
        "data": {
            "id": dummy_data["id"],
            "nickname": dummy_data["nickname"],
            "dark_mode": dummy_data["dark_mode"],
            "notification": dummy_data["notification"]
        }
    }

