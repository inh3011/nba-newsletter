from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone

from app.models.user import UserCreate, UserOut
from app.models.api import APIResponse
from app.core.dynamodb import get_table
from app.services import teams as team_service

import traceback
import os

router = APIRouter()
TABLE_NAME = os.getenv("USERS_TABLE_NAME", "users")

@router.get("/subscribers", response_model=APIResponse[list[UserOut]])
def list_subscribers():
    """
    Get all newsletter subscribers.
    """
    table = get_table(TABLE_NAME)
    
    try:
        response = table.scan()
        items = response.get("Items", [])
        return APIResponse.success_response(items, "Successfully retrieved subscribers")
    except Exception as e:
        return APIResponse.error_response(str(e), "Failed to retrieve subscribers")


@router.post("/subscribe", response_model=APIResponse[UserOut])
def register_user(user: UserCreate):
    """
    Subscribe to the newsletter or retrieve existing user.
    """
    table = get_table(TABLE_NAME)

    try:
        # Check for existing user with the same email
        existing_user = table.get_item(Key={"email": user.email}).get("Item")
        if existing_user:
            # Instead of returning an error, return the existing user with a different message
            return APIResponse.success_response(existing_user, "Existing user retrieved")

        # If user doesn't exist, create new user
        item = {
            "email": user.email,
            "teams": [],
            "players": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

        table.put_item(Item=item)
        return APIResponse.success_response(item, "User registered successfully")
    except Exception as e:
        return APIResponse.error_response(str(e), "Failed to register user")


@router.get("/subscribe/{email}", response_model=APIResponse[UserOut])
def get_user(email: str):
    """
    Retrieve newsletter subscription info by email.
    """
    table = get_table(TABLE_NAME)

    try:
        response = table.get_item(Key={"email": email})
        item = response.get("Item")

        if not item:
            return APIResponse.error_response("User not found", "Retrieval failed")

        return APIResponse.success_response(item, "User retrieved successfully")
    except Exception as e:
        return APIResponse.error_response(str(e), "Failed to retrieve user")

@router.patch("/{email}/teams", response_model=APIResponse[UserOut])
def update_user_teams(email: str, team_ids: list[int]):
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
            if team['id'] in team_ids
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
        return APIResponse.success_response(response["Attributes"], "Teams updated successfully")

    except Exception as e:
        print("[ERROR] update_user_teams failed:", e)
        traceback.print_exc()
        return APIResponse.error_response(str(e), "Failed to update teams")

@router.delete("/unsubscribe/{email}", response_model=APIResponse[dict])
def delete_user(email: str):
    """
    Unsubscribe from the newsletter.
    """
    table = get_table(TABLE_NAME)
    
    try:
        table.delete_item(Key={"email": email})
        return APIResponse.success_response({"email": email}, "Successfully unsubscribed user")
    except Exception as e:
        return APIResponse.error_response(str(e), "Failed to unsubscribe user")