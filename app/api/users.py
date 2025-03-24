from fastapi import APIRouter
from app.models.user import User

router = APIRouter()

@router.post("/register")
def register_user(user: User):
    print(f"등록된 사용자: {user.email}, 관심 선수: {user.players}")
    return {"message": "등록 성공 (DB 연동 예정)"}