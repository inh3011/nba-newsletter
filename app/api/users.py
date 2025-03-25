from fastapi import APIRouter, HTTPException
from app.models.user import UserCreate, UserOut
from app.core.dynamodb import get_table
from datetime import datetime, timezone
import os

router = APIRouter()
TABLE_NAME = os.getenv("USERS_TABLE_NAME", "users")


@router.post("/subscribe", response_model=UserOut)
def register_user(user: UserCreate):
    table = get_table(TABLE_NAME)
    now = datetime.now(timezone.utc).isoformat()

    item = {
        "email": user.email,
        "created_at": now,
        "updated_at": now
    }

    try:
        table.put_item(Item=item)
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/subscribe/{email}", response_model=UserOut)
def get_user(email: str):
    table = get_table(TABLE_NAME)

    try:
        response = table.get_item(Key={"email": email})
        item = response.get("Item")

        if not item:
            raise HTTPException(status_code=404, detail="User not found")

        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.put("/users/{email}")
# def update_user(email: str, user: User):
#     table = get_table(TABLE_NAME)
    
#     try:
#         response = table.update_item(
#             Key={"email": email},
#             UpdateExpression="set timezone=:tz",
#             ExpressionAttributeValues={":tz": user.timezone},
#             ReturnValues="ALL_NEW"
#         )
#         return response["Attributes"]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.delete("/unsubscribe/{email}")
def delete_user(email: str):
    table = get_table(TABLE_NAME)
    
    try:
        table.delete_item(Key={"email": email})
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))