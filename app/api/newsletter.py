from fastapi import APIRouter

router = APIRouter()

@router.get("")
def test_newsletter():
    return {"message": "뉴스레터 테스트"}