from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone

from app.models.user import UserCreate, UserOut
from app.core.dynamodb import get_table
from app.services import teams as team_service

import traceback
import os

router = APIRouter()
TABLE_NAME = os.getenv("USERS_TABLE_NAME", "users")

@router.post("/subscribe", response_model=UserOut)
def register_user(user: UserCreate):
    """
    Subscribe to the newsletter.
    """
    table = get_table(TABLE_NAME)
    item = {
        "email": user.email,
        "teams": [],
        "players": [],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    try:
        table.put_item(Item=item)
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/subscribe/{email}", response_model=UserOut)
def get_user(email: str):
    """
    Retrieve newsletter subscription info by email.
    """
    table = get_table(TABLE_NAME)

    try:
        response = table.get_item(Key={"email": email})
        item = response.get("Item")

        if not item:
            raise HTTPException(status_code=404, detail="User not found")

        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{email}/teams", response_model=UserOut)
def update_user_teams(email: str, team_names: list[str]):
    """
    Update the list of favorite teams for the newsletter.
    """
    table = get_table(TABLE_NAME)
    try:
        all_teams = team_service.get_team_list()

        selected = [
            {
                "id": team['id'],
                "name": team['full_name'],
                "abbreviation": team['abbreviation']
            }
            for team in all_teams
            if team['full_name'] in team_names
        ]


        response = table.update_item(
            Key={"email": email},
            UpdateExpression="SET teams = :teams, updated_at = :updated_at",
            ExpressionAttributeValues={
                ":teams": selected,
                ":updated_at": datetime.now(timezone.utc).isoformat()
            },
            ReturnValues="ALL_NEW"
        )
        return response["Attributes"]

    except Exception as e:
        print("[ERROR] update_user_teams failed:", e)
        traceback.print_exc()

        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/unsubscribe/{email}")
def delete_user(email: str):
    """
    Unsubscribe from the newsletter.
    """
    table = get_table(TABLE_NAME)
    
    try:
        table.delete_item(Key={"email": email})
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))