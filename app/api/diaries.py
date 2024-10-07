from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import List, Optional
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/diaries")


class Mood(Enum):
    SMILE = 1
    SAD = 2
    MEDIOCRE = 3
    ANGRY = 4
    EXCITED = 5
    HAPPY = 6


class Weather(Enum):
    SUNNY = 1
    RAINY = 2
    SNOWY = 3
    THUNDERSTORM = 4
    CLOUDY = 5
    WINDY = 6


class Diary(BaseModel):
    id: int | None = None
    date: str
    mood: Mood | str
    weather: Weather | str
    title: str
    image: str | None = None
    story: str


class TempDiary(BaseModel):
    id: int | None = None
    date: str | None = None
    mood: Mood | str | None = None
    weather: Weather | str | None = None
    title: str | None = None
    image: str | None = None
    story: str | None = None



diaries_db = []
diary_id_counter = 1
fixed_nickname = "팡팡이"

# 다이어리 작성 API
@router.post("", status_code=201)
async def save_diary(diary: Diary):
    global diary_id_counter

    # 다이어리 정보를 저장
    diary_entry = {
        "id": diary_id_counter,
        "date": diary.date,
        "nickname": fixed_nickname,
        "mood": diary.mood,
        "weather": diary.weather,
        "title": diary.title,
        "image": diary.image,  # 선택적 필드
        "story": diary.story,
    }
    diaries_db.append(diary_entry)

    # ID 증가
    diary_id_counter += 1

    return {
        "status": 201,
        "message": "다이어리 저장 성공",
        "id": diary_entry["id"]
    }



@router.put("/{id}")
async def edit_diary(id: int, diary: Diary):
    # 다이어리 ID가 존재하는지 확인
    existing_diary = next((d for d in diaries_db if d["id"] == id), None)
    if existing_diary is None:
        raise HTTPException(status_code=404, detail=f"다이어리 ID {id}이 존재하지 않습니다.")

    # 필수 요소 체크
    missing_fields = []
    
    if not diary.title:
        missing_fields.append("title")
    if not diary.date:
        missing_fields.append("date")
    if not diary.mood:
        missing_fields.append("mood")
    if not diary.weather:
        missing_fields.append("weather")
    if not diary.story:
        missing_fields.append("story")

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"다이어리를 수정하지 못했습니다. 필수 요소({', '.join(missing_fields)})가 누락되었습니다."
        )

    # 기존 다이어리 수정
    existing_diary.update({
        "date": diary.date,
        "title": diary.title,
        "image": diary.image,
        "mood": diary.mood,
        "weather": diary.weather,
        "story": diary.story,
    })

    return {
        "status": 200,
        "message": "다이어리 수정 성공",
        "id": id
    }


# 임시 다이어리 저장소
temp_diaries_db = []
temp_id_counter = 20  # 임시 다이어리 ID 시작값

@router.post("/diaries/temp", status_code=200)
async def save_temp_diary(temp_diary: TempDiary):
    global temp_id_counter

    # 임시 다이어리 정보 저장
    temp_diary_entry = {
        "temp_id": temp_id_counter,
        "date": temp_diary.date,
        "nickname": fixed_nickname,
        "mood": temp_diary.mood,
        "weather": temp_diary.weather,
        "image": temp_diary.image,
        "story": temp_diary.story,
    }
    
    # 임시 다이어리 저장소에 추가
    temp_diaries_db.append(temp_diary_entry)

    # ID 증가
    temp_id_counter += 1

    return {
        "status": 200,
        "message": "다이어리 임시 저장 성공",
        "temp_id": temp_diary_entry["temp_id"]
    }


# /diaries?date=20240909
@router.get("")
async def search_diary_exist(date: int = Query(..., description="조회할 날짜 (예: 20240909)")):
    if date == 20240909:
        return {
            "status": 200,
            "message": "작성한 다이어리가 존재합니다.",
            "data": {"date": "2024-09-09", "is_exist": True, "id": 30},
        }
    elif date == 20240910:
        return {
            "status": 200,
            "message": "작성한 다이어리가 존재합니다.",
            "data": {"date": "2024-09-10", "is_exist": True, "id": 31},
        }
    # 다른 날짜 추가
    return {
        "status": 200,
        "message": "작성한 다이어리가 존재하지 않습니다.",
        "data": {"date": str(date), "is_exist": False, "id": 55},
    }





# /diaries/{id}
@router.delete("/{id}")
async def delete_diary(id: int):
    return {"status": 200, "message": f"{id}번 다이어리 삭제 성공"}


# /diaries/like/{id}
@router.put("/like/{id}")
async def like_diary(id: int):
    # id가 999인 경우 좋아요 취소
    if id == 999:
        return {"status": 200, "id": 999, "bookmark": False}
    return {"status": 200, "id": id, "bookmark": True}


# /diaries/search?keyword={keyword}
@router.get("/search")
async def search_diary(keyword: str = Query("", description="검색 키워드")):
    if keyword == "":
        return {"status": 200, "message": "모든 다이어리 조회"}

    if keyword == "999":
        return {"status": 404, "message": "해당 키워드로 검색이 되지 않았습니다."}

    return {
        "status": 200,
        "message": f"{keyword}에 관한 일기 조회 완료",
        "data": [
            {
                "id": 1,
                "date": "2024-08-13",
                "title": f"신나는 {keyword}을 했따",
                "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...AYH/",
                "bookmark": 1,
            },
            {
                "id": 3,
                "date": "2024-08-20",
                "title": f"{keyword} 가기 싫다",
                "image": None,
                "bookmark": 0,
            },
        ],
    }



# 더미
diaries_list = [
    {
        "id": 1,
        "date": "2024-08-13",
        "title": "신나는 산책을 했따",
        "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...AYH/",
        "bookmark": True
    },
    {
        "id": 2,
        "date": "2024-01-19",
        "title": "캬캬캬캬캬",
        "image": "base64파일이 들어갈 자리",  # 이미지가 없는 경우
        "bookmark": True
    },
    {
        "id": 3,
        "date": "2025-12-19",
        "title": "운동 가기 귀찮다 배드민턴 재밌다",
        "image": None,  # 이미지가 없는 경우
        "bookmark": True
    },
    {
        "id": 4,
        "date": "2023-09-10",
        "title": "쿨쿨핑",
        "image": "base64파일이 들어갈 자리",  # 이미지가 없는 경우
        "bookmark": True
    },
    {
        "id": 5,
        "date": "2024-09-11",
        "title": "냠냠 맛있는거 먹기",
        "image": "base64파일이 들어갈 자리",  # 이미지가 없는 경우
        "bookmark": True
    }
]


@router.get("/like")
async def get_like_diaries(
    type: str = Query(..., description="필터 타입, 'all' 또는 'month'"),
    date: str = Query(None, description="연월 필터 (형식: YYYYMM)")
):

    # 타입이 'all'인 경우: 모든 북마크된 일기를 반환
    if type == "all":
        liked_diaries = [diary for diary in diaries_list if diary["bookmark"]]
        
        # 최신 날짜 순으로 정렬 (가장 최근 날짜가 처음에 오도록)
        liked_diaries = sorted(liked_diaries, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)
        
        message = "좋아요 누른 모든 일기 조회 완료"
    
    # 타입이 'month'인 경우: 특정 연월(date)의 북마크된 일기를 필터링하여 반환
    elif type == "month":
        if not date or len(date) != 6:
            raise HTTPException(status_code=400, detail="올바른 연월(YYYYMM) 형식으로 입력해주세요.")
        
        year = date[:4]
        month = date[4:]
        
        liked_diaries = [
            diary for diary in diaries_list 
            if diary["bookmark"] and diary["date"].startswith(f"{year}-{month}")
        ]
        message = f"{year}년 {month}월 좋아요 누른 일기 조회 완료"
    else:
        raise HTTPException(status_code=400, detail="잘못된 type 값입니다. 'all' 또는 'month'로 요청하세요.")
    
    if not liked_diaries:
        raise HTTPException(status_code=404, detail="좋아요를 누른 다이어리가 없습니다.")

    return {
        "status": 200,
        "message": message,
        "data": liked_diaries,
    }



from datetime import datetime
from fastapi import Query
from fastapi.responses import JSONResponse

diaries_db = [
    {
        "id": 1,
        "date": "2024-08-13",
        "title": "8월 두번째",
        "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...AYH/",
        "bookmark": True
    },
    {
        "id": 2,
        "date": "2024-09-29",
        "title": "9월 세번째",
        "image": None,
        "bookmark": False
    },
    {
        "id": 3,
        "date": "2024-08-09",
        "title": "8월 첫번째",
        "image": None,
        "bookmark": True
    },
    {
        "id": 4,
        "date": "2024-09-09",
        "title": "9월 두번째",
        "image": None,
        "bookmark": True
    },
    {
        "id": 5,
        "date": "2024-08-30",
        "title": "8월 세번째",
        "image": None,
        "bookmark": False
    },
    {
        "id": 6,
        "date": "2024-09-01",
        "title": "9월 첫번째",
        "image": None,
        "bookmark": False
    }
]

# /diaries/main?type=calender&date=202406
# /diaries/main?type=list&date=202406
@router.get("/main")
async def get_main_diaries(type: str = Query(..., description="조회 유형 (list 또는 calender)"),
                           date: str = Query(..., description="조회할 년월 (예: 202408)")):
    # date 파라미터의 형식을 검증 (6자리 숫자)
    if len(date) != 6 or not date.isdigit():
        return JSONResponse(content={
            "status": 400,
            "message": "날짜 형식이 잘못되었습니다. YYYYMM 형식이어야 합니다."
        })

    # 다이어리 데이터를 날짜 기준으로 필터링
    filtered_diaries = [diary for diary in diaries_db if diary["date"].startswith(date[:4] + "-" + date[4:])]

    # type이 "calender"인 경우: 오래된 순으로 정렬
    if type == "calender":
        calendar_data = sorted(
            [
                {
                    "id": diary["id"],
                    "date": diary["date"],
                    "image": diary["image"],
                    "bookmark": diary["bookmark"]
                }
                for diary in filtered_diaries
            ],
            key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"),  # 날짜 기준으로 정렬
            reverse=False  # 오래된 순
        )
        return JSONResponse(content={
            "status": 200,
            "message": "다이어리 캘린더형 조회 완료",
            "data": calendar_data
        })

    # type이 "list"인 경우: 최신순으로 정렬
    elif type == "list":
        list_data = sorted(
            [
                {
                    "id": diary["id"],
                    "date": diary["date"],
                    "title": diary["title"],
                    "image": diary["image"],
                    "bookmark": diary["bookmark"]
                }
                for diary in filtered_diaries
            ],
            key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"),  # 날짜 기준으로 정렬
            reverse=True  # 최신순
        )
        return JSONResponse(content={
            "status": 200,
            "message": "다이어리 목록형 조회 완료",
            "data": list_data
        })

    # 잘못된 type인 경우
    return JSONResponse(content={
        "status": 400,
        "message": "잘못된 조회 유형입니다. 'list' 또는 'calender'를 사용하세요."
    })


@router.get("/{id}")
async def get_diary(id: int, edit: str = None):
    # id가 999인 경우 존재하지 않는 다이어리
    if id == 999:
        return {
            "status": 404,
            "message": f"id가 {id}인 다이어리가 존재하지 않음",
        }

    # edit을 수동으로 bool로 변환
    is_edit = edit.lower() == "true" if edit else False

    # edit 이 True 경우 수정 중인 것으로 리턴
    if is_edit:
        return {
            "status": 200,
            "message": f"{id}번 다이어리 수정 준비 완료",
            "data": {
                "id": 1,
                "date": "2024-08-13",
                "nickname": "팡팡이",
                "mood": 1,
                "weather": 3,
                "title": "신나는 산책을 했따",
                "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...AYH/",
                "story": "아침에 쿨쿨자고 ,,,,",
            },
            "temp_id": 55,
        }
    
    return {
        "status": 200,
        "message": f"{id}번 다이어리 조회 완료",
        "data": {
            "id": 1,
            "date": 20240813,
            "nickname": "팡팡이",
            "mood": 1,
            "weather": 3,
            "title": "신나는 산책을 했따",
            "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...AYH/",
            "story": "아침에 쿨쿨자고 ,,,,",
        },
    }
